# Receipt Processor API

A RESTful API for processing retail receipts, calculating reward points, and retrieving points associated with a receipt.

---

## **Installation and Setup**

Follow these steps to set up the project on your local machine.

### **1. Prerequisites**
Ensure you have the following installed:
- **Python 3.9+**
- **pip** (Python package manager)

---

### **2. Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/pramodreddypandiri/receipt-processor.git
cd receipt-processor

```

### 3. Set Up a Virtual Environment 
Create a virtual environment to isolate project dependencies:

```bash

python3 -m venv venv
```

Activate the virtual environment:

On macOS/Linux:

```bash

source venv/bin/activate
```
On Windows:

```bash

venv\Scripts\activate
```
### 4. Install Dependencies
Install the required Python packages using pip:


```bash

pip install -r requirements.txt
```
or 


```bash

pip3 install -r requirements.txt
```

### Running the API
Start the API server using Uvicorn:

bash
```
uvicorn main:app --reload
```
or 

Run main.py file
```bash
python3 main.py
```
By default, The server will be running at: http://127.0.0.1:8000

### Note:
Go to  http://127.0.0.1:8000/docs to make use of FastAPI- SwaggerUI to use/test api.
