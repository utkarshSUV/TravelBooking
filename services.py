from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models import Member, Inventory, Booking
from datetime import datetime, timezone
import pandas as pd
from io import StringIO


# Service to handle booking an item
def book_item(db: Session, member_id: int, inventory_id: int):
    try:
        # Find member and inventory
        member = db.query(Member).filter(Member.id == member_id).first()
        inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
        if inventory is None:
            return {"error": "Inventory not found"}
        if member is None:
            return {"error": "Member not found"}

        if member and inventory:
            # Check if current date is less than inventory expiration date
            current_date = datetime.now(timezone.utc)
            if current_date > inventory.expiration_date:
                return {"error": "Inventory has expired, cannot book this item."}
            # Check if member has reached max bookings (2) and inventory count is not 0
            if member.booking_count < 2 and inventory.remaining_count > 0:
                new_booking = Booking(member_id=member_id, inventory_id=inventory_id)
                db.add(new_booking)
                db.commit()

                # Update booking count and inventory remaining count
                member.booking_count += 1
                inventory.remaining_count -= 1

                db.commit()
                return {"message": "Booking successful"}
            else:
                return {"error": "Booking limit reached or item out of stock"}

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return {"SQLAlchemy_Error": "A database connection error occurred. Please try again later."}
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {"unexpected_error": "An unexpected error occurred. Please try again later."}


# Service to cancel a booking
def cancel_booking(db: Session, booking_id: int):
    try:
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if booking:
            # Cancel the booking and restore inventory
            member = booking.member
            inventory = booking.inventory

            db.delete(booking)
            db.commit()

            # Update counts
            member.booking_count -= 1
            inventory.remaining_count += 1
            db.commit()

            return {"message": "Booking cancelled"}
        else:
            return {"error": "Booking not found"}

    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return {"SQLAlchemy_Error": "A database connection error occurred. Please try again later."}
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {"unexpected_error": "An unexpected error occurred. Please try again later."}


# Service to upload members from a CSV file
def upload_members(file_content: bytes, db: Session):
    # Decode byte content and read into a pandas DataFrame
    file_str = file_content.decode("utf-8")  # Convert bytes to a string
    try:
        data = pd.read_csv(StringIO(file_str))  # Read CSV data into pandas DataFrame
    except Exception as e:
        return {"error": "Error reading CSV file: " + str(e)}

    # Validation for required columns
    required_columns = ['name', 'surname', 'booking_count', 'date_joined']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return {"error": f"CSV is missing required columns: {', '.join(missing_columns)}"}

    # Validate and parse 'date_joined' column
    for index, row in data.iterrows():
        try:
            # Validate and parse 'date_joined' in ISO format (e.g., 2024-01-02T12:10:11)
            try:
                date_joined = datetime.fromisoformat(row['date_joined'].strip())
            except Exception as e:
                return {"error": f"Invalid date format in row {index}: {row['date_joined']}"}

                # Check if a member with the same name and surname already exists in the database
            existing_member = db.query(Member).filter(
                Member.name == row['name'], Member.surname == row['surname']).first()

            if existing_member:
                print(
                    f"Skipping row {index} as member with name {row['name']} and surname {row['surname']} already exists.")
                continue  # Skip this row if the member already exists in the database

            db.add(Member(
                name=row['name'],
                surname=row['surname'],
                booking_count=int(row['booking_count']),
                date_joined=date_joined  # Using parsed datetime
            ))
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Error: {e}")
            return {"SQLAlchemy_Error": "A database connection error occurred. Please try again later."}
        except Exception as e:
            return {"error": f"Error processing row {index}: {str(e)}"}

    try:
        db.commit()
    except Exception as e:
        db.rollback()  # Rollback in case of any failure during commit
        return {"SQLAlchemy_Error": f"Error committing to the database: {str(e)}"}
    return {"message": "Members uploaded successfully"}


# Service to upload inventory from a CSV file
def upload_inventory(file_content: bytes, db: Session):
    # Decode byte content and read into a pandas DataFrame
    file_str = file_content.decode("utf-8")  # Convert bytes to a string
    try:
        data = pd.read_csv(StringIO(file_str))  # Read CSV data into pandas DataFrame
    except Exception as e:
        return {"error": "Error reading CSV file: " + str(e)}

    # Validation for required columns
    required_columns = ['title', 'description', 'remaining_count', 'expiration_date']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        return {"error": f"CSV is missing required columns: {', '.join(missing_columns)}"}

    # Validate and parse 'expiration_date' column
    for index, row in data.iterrows():
        try:
            # Validate and parse 'expiration_date' in format DD/MM/YYYY (e.g., 19/11/2030)
            try:
                expiration_date = datetime.strptime(row['expiration_date'].strip(), "%d/%m/%Y")
            except ValueError:
                return {"error": f"Invalid date format in row {index}: {row['expiration_date']}"}
            existing_inventory = db.query(Inventory).filter(Inventory.title == row['title']).first()

            if existing_inventory: # If existing inventory then update that data
                print(
                    f"already existing inventory for row {index}, Now updating inventory for 'Title'-> {row['title']} with latest csv values")
                existing_inventory.title = row['title']
                existing_inventory.description = row['description']
                existing_inventory.remaining_count = row['remaining_count']
                existing_inventory.expiration_date = row['expiration_date']
                db.add(existing_inventory)
                continue  # Skip this row if the member already exists in the database
            db.add(Inventory(
                title=row['title'],
                description=row['description'],
                remaining_count=int(row['remaining_count']),
                expiration_date=expiration_date  # Using parsed datetime
            ))
        except SQLAlchemyError as e:
            print(f"SQLAlchemy Error: {e}")
            return {"SQLAlchemy_Error": "A database connection error occurred. Please try again later."}

        except Exception as e:
            return {"error": f"Error processing row {index}: {str(e)}"}

    db.commit()
    return {"message": "Inventory uploaded successfully"}
