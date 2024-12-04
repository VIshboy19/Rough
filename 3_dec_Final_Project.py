from ultralytics import YOLO
from pymongo import MongoClient
import cv2
import numpy as np


# Initialize YOLO model and MongoDB connection
model = YOLO("yolov8s.pt")
uri = "mongodb://localhost:27017"
client = MongoClient(uri)
tt = client["car_databases"]
gg = tt["car_colorss"]

# Paths to images
loc = r"C:\Users\vishr\OneDrive\Desktop\captured_image2.jpeg"
loc2 =r"C:\Users\vishr\OneDrive\Desktop\captured_image1.jpeg"

# Function to generate dictionary with detected objects
def get_dict(locc):
    label_dict = {}
    results = model(locc)  # Run inference on the image
    image = cv2.imread(locc)

    if image is None:
        print("Error loading the image. Please check the file path.")
        return label_dict

    for result in results:
        boxes = result.boxes
        if boxes is not None:
            xyxy_boxes = boxes.xyxy.cpu().numpy()  # Bounding boxes
            
            # Sort boxes based on the leftmost x-coordinate (x1)
            sorted_boxes = sorted(xyxy_boxes, key=lambda box: box[0])
            
            for idx, box in enumerate(sorted_boxes):
                inf = input(f"Enter book name : ").strip().lower()
                x1, y1, x2, y2 = map(int, box)

                # Add to dictionary
                label_dict[inf] = {"location": [x1, y1, x2, y2], "loaned": "no"}
                
                # Slice and display ROI
                #roi = image[y1:y2, x1:x2]
                #if roi.size > 0:  # Ensure ROI is valid
                #    cv2.imshow(f"ROI {idx+1} - {inf}", roi)
                #    cv2.waitKey(8000)  # Show each ROI for 2 seconds
                #    cv2.destroyWindow(f"ROI {idx+1} - {inf}")
                #else:
                #    print(f"Invalid ROI for box {idx+1}: {box}")
                
    return label_dict


# Function to upload data to MongoDB
def uploadData(di):
    if not di:
        print("No data to upload.")
        return
    documents = [{'color': key, 'details': value} for key, value in di.items()]
    result = gg.insert_many(documents)
    print("Inserted document IDs:", result.inserted_ids)

# Function to update loan status in MongoDB
def update_info():
    color = input("Enter the book you want to loan: ").strip().lower()
    filter_query = {"color": color}
    update_query = {"$set": {"details.loaned": "yes"}}
    results = gg.update_many(filter_query, update_query)
    if results.matched_count > 0:
        updated_docs = {doc["color"]: doc for doc in gg.find(filter_query)}
        print("Book loaned. Please take the book away.")
        return updated_docs
    else:
        print(f"No documents found with color '{color}'.")


# Function to retrieve all data from MongoDB as a dictionary
def fetch_all_data():
    all_data = {}
    for doc in gg.find():
        color = doc.get("color", "")
        details = doc.get("details", {})
        all_data[color] = {"details": details}
    return all_data


# Function to visualize regions of interest in two images
def check_pic(tt, loc1, loc2):
    
    # Get book name from user
    color_name = input("Enter which book you want to see: ").lower()
    
    # Check if the book exists in the data
    if color_name not in tt:
        print(f"Book '{color_name}' not found.")
        return  # Exit the function if the book is not found

    # Extract book details
    details = tt[color_name]["details"]
    pixel_array = details.get("location", [])
    
    # Validate coordinates
    if not pixel_array or len(pixel_array) != 4:
        print(f"Invalid coordinates for '{color_name}'.")
        return
    
    x1, y1, x2, y2 = map(int, pixel_array)
    imga = cv2.imread(loc1)
    imgb = cv2.imread(loc2)

    if imga is None or imgb is None:
        print("Error loading images. Please check file paths.")
        return

    # Extract ROIs
    roi = imga[y1:y2, x1:x2]
    roi2 = imgb[y1:y2, x1:x2]

    loan_status = details.get("loaned", "no")

    # Run YOLO on ROIs
    try:
        yroi1 = model(roi)
        yroi2 = model(roi2)
    except Exception as e:
        print(f"Error during model inference: {e}")
        return

    boxes1 = yroi1[0].boxes if len(yroi1) > 0 else None
    boxes2 = yroi2[0].boxes if len(yroi2) > 0 else None

    # Determine loan status
    if loan_status == "yes":
        if boxes1 or boxes2:
            print("Problem: Book is loaned but still available.")
        else:
            print("No problem: Book is loaned and not available.")
    else:
        if not boxes1 and not boxes2:
            print("Problem: Book is not loaned but not available.")
        else:
            print("No problem: Book is not loaned and is available.")

    # Optional visualization
    cv2.imshow("ROI from Image 1", roi)
    cv2.imshow("ROI from Image 2", roi2)
    cv2.waitKey(8000)
    cv2.destroyAllWindows()



# Update the `main` function to fetch all data after updating loan status
if __name__ == "__main__":
    # Generate dictionary from YOLO detections
    detected_data = get_dict(loc)

    # Upload data to MongoDB
    uploadData(detected_data)

    # Update loan status
    update_info()

    # Retrieve the updated data from the database
    all_data = fetch_all_data()

    # Visualize selected color regions
    check_pic(all_data, loc, loc2)