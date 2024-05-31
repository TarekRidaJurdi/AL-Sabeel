from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, MetaData, Table, select, column, literal_column
from databases import Database
import uvicorn
import sqlite3
from fastapi.responses import RedirectResponse, HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

class Storage:
    status=''

#functions 
def convert_dicts_to_tuples(list_of_dicts):
    # Initialize an empty list to store tuples
    tuples_list = []

    # Iterate over each dictionary in the list
    for dictionary in list_of_dicts:
        # Create a tuple containing the values of the dictionary
        # and append it to the list of tuples
        tuples_list.append(tuple(dictionary.values())[:-1])

    return tuples_list
def remove_first_n_elements(data_list,n):
    result = []
    for item in data_list:
        result.append(item[n:])  
    return result
def check_record_exists(national_num):
    conn = sqlite3.connect('alsabeel_data.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM family
                      WHERE national_num = ? OR national_num_w = ?''', (national_num, national_num))

    record = cursor.fetchone()

    conn.close()

    return record is not None
def display_family_record(family_id):
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()

    # Retrieve family data
    cursor.execute("SELECT * FROM family WHERE id=?", (family_id,))
    family_data = cursor.fetchone()
    
    # Retrieve children data
    cursor.execute("SELECT * FROM children WHERE family_id=?", (family_id,))
    children_data = cursor.fetchall()
    
    # Retrieve assistance data
    cursor.execute("SELECT * FROM assistance WHERE family_id=?", (family_id,))
    assistance_data = cursor.fetchall()
    
    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()
    children_data=remove_first_n_elements(children_data,1)
    assistance_data=remove_first_n_elements(assistance_data,1)
    return family_data,children_data,assistance_data
def delete_family_record(family_id):
    try:
        # Connect to the database
        connection = sqlite3.connect('alsabeel_data.db')
        cursor = connection.cursor()

        # Delete records from the children table associated with the family
        cursor.execute("DELETE FROM children WHERE family_id=?", (family_id,))

        # Delete records from the assistance table associated with the family
        cursor.execute("DELETE FROM assistance WHERE family_id=?", (family_id,))

        # Delete record from the family table
        cursor.execute("DELETE FROM family WHERE id=?", (family_id,))

        # Commit the changes
        connection.commit()

        # Close the cursor
        cursor.close()

        # Close the connection
        connection.close()

        print("Family record and associated data deleted successfully.")
    except Exception as e:
        print("An error occurred:", e)

def insert_family_data(data):
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()
    
    # Extracting required data from the input dictionary
    required_data = (
        data['formData']['husband'], data['formData']['father'], data['formData']['family'],
        data['formData']['birthday'], data['formData']['nationalNum'], data['formData']['job'],
        data['formData']['wife'], data['formData']['father-w'], data['formData']['family-w'],
        data['formData']['birthday-w'], data['formData']['nationalNum-w'], data['formData']['job-w'],
        data['formData']['state'], data['formData']['city'], data['formData']['village'],
        data['formData']['specificPoint'], data['formData']['house'], data['formData']['livingStatus'],
        data['formData']['basicMobile'], data['formData']['alternativeMobile'], data['formData']['telephone'],
        data['formData']['familyHealth'], data['formData']['additionalInfo'], data['formData']['statusSource'],
        data['formData']['regDate'], data['formData']['applicant'], data['formData']['dataEntrier'],
        data['formData']['applicantEvaluation'], data['formData']['evaluationText'], 
        data['formData']['managementNotes'],data['formData']['status'],
        data['formData']['status_1'],data['formData']['study_response'],data['formData']['income']
    )

    cursor.execute("""
        INSERT INTO family (
            husband, father, family, birthday, national_num, job, 
            wife, father_w, family_w, birthday_w, national_num_w, job_w,
            state, city, village, specific_point, house, living_status,
            basic_mobile, alternative_mobile, telephone, family_health,
            additional_info, status_source, reg_date, applicant,
            data_entrier, applicant_evaluation, evaluation_text, management_notes,status,status_1,study_response,income
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
    """, required_data)

    family_id = cursor.lastrowid

    cursor.close()
    connection.commit()
    connection.close()

    return family_id
def insert_children_data(family_id, children_data):
    # Connect to the database
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()

    # Insert records into the children table
    cursor.executemany("""
        INSERT INTO children (family_id,child_name, birthday_child, study_work, notes)
        VALUES (?, ?, ?, ?, ?)
    """, [(family_id,) + child for child in children_data])

    # Close the cursor
    cursor.close()

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
def insert_assistance_data(family_id, assistance_data):
    # Connect to the database
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()

    # Insert records into the assistance table
    cursor.executemany("""
        INSERT INTO assistance (family_id, assistance_value, assistance_date)
        VALUES (?, ?, ?)
    """, [(family_id,) + assistance for assistance in assistance_data])

    # Close the cursor
    cursor.close()

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
def get_latest_assistance_info():
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()

    query = """
        SELECT family.id, family.husband,family.family,family.status,family.basic_mobile,family.state ,family.city,family.village,family.specific_point,  
               family.reg_date, MAX(assistance.assistance_date) AS latest_assistance_date , family.study_response
        FROM family
        LEFT JOIN assistance ON family.id = assistance.family_id
        GROUP BY family.id
        ORDER BY family.id DESC
    """

    cursor.execute(query)

    latest_assistance_info = cursor.fetchall()
    records_length=len(latest_assistance_info)
    cursor.close()
    connection.close()
    return {'records':latest_assistance_info[:130],'length':records_length}
def get_latest_assistance_info_with_filter(filters=None):
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()

    filter_clause = ""
    filter_values = ()
    if filters:
        filter_fields = []
        for filter_field, filter_value in filters.items():
            filter_fields.append(f"{filter_field} LIKE ?")
        filter_clause = " WHERE " + " AND ".join(filter_fields)
        filter_values = tuple([f"%{filter_value}%" for _, filter_value in filters.items()])

    query = f"""
        SELECT family.id, family.husband,family.family, family.status, family.basic_mobile, family.state,family.city, family.village, family.specific_point,  
               family.reg_date, MAX(assistance.assistance_date) AS latest_assistance_date, family.study_response
        FROM family
        LEFT JOIN assistance ON family.id = assistance.family_id
        {filter_clause}
        GROUP BY family.id
        ORDER BY family.id DESC
    """
    
    cursor.execute(query, filter_values)

    latest_assistance_info = cursor.fetchall()
    records_length=len(latest_assistance_info)
    cursor.close()
    connection.close()
    return {'records':latest_assistance_info[:130],'length':records_length}

def get_latest_assistance_info_with_family_id(family_id):
    connection = sqlite3.connect('alsabeel_data.db')
    cursor = connection.cursor()

    query = """
        SELECT 
            family.id,
            family.husband,
            family.family,
            family.status,
            family.basic_mobile,
            family.state,
            family.city,
            family.village,
            family.specific_point,
            family.reg_date,
            MAX(assistance.assistance_date) AS latest_assistance_date,
            family.study_response
        FROM 
            family
        LEFT JOIN 
            assistance ON family.id = assistance.family_id
        WHERE 
            family.id=?
        GROUP BY 
            family.id,
            family.husband,
            family.family,
            family.status,
            family.basic_mobile,
            family.state,
            family.city,
            family.village,
            family.specific_point,
            family.reg_date,
            family.study_response
        ORDER BY 
            family.id DESC
    """
    
    cursor.execute(query, (family_id,))

    latest_assistance_info = cursor.fetchall()
    records_length = len(latest_assistance_info)
    cursor.close()
    connection.close()
    return {'records': latest_assistance_info[:130], 'length': records_length}
def update_family_data(family_id, new_data):
    try:
        # Connect to the database
        connection = sqlite3.connect('alsabeel_data.db')
        cursor = connection.cursor()

        # Update record in the family table
        cursor.execute("""
            UPDATE family
            SET husband=?, father=?, family=?, birthday=?, national_num=?, job=?,
            wife=?, father_w=?, family_w=?, birthday_w=?, national_num_w=?, job_w=?,
            state=?, city=?, village=?, specific_point=?, house=?, living_status=?,
            basic_mobile=?, alternative_mobile=?, telephone=?, family_health=?,
            additional_info=?, status_source=?, reg_date=?, applicant=?,
            data_entrier=?, applicant_evaluation=?, evaluation_text=?, management_notes=?,status=?,status_1=?,study_response=?,income=?
            WHERE id=?
        """, new_data + (family_id,))

        # Commit the changes
        connection.commit()

        # Close the cursor
        cursor.close()

        # Close the connection
        connection.close()

        print("Family data updated successfully.")
    except Exception as e:
        print("An error occurred:", e)

def update_children_data(family_id, new_children_data):
    try:
        # Connect to the database
        connection = sqlite3.connect('alsabeel_data.db')
        cursor = connection.cursor()
        # Delete records from the children table associated with the family
        cursor.execute("DELETE FROM children WHERE family_id=?", (family_id,))
        # Commit the changes
        connection.commit()
        # Close the cursor
        cursor.close()
        # Close the connection
        connection.close()
        insert_children_data(family_id, new_children_data)

        print("Children data updated successfully.")
    except Exception as e:
        print("An error occurred:", e)

def update_assistance_data(family_id, new_assistance_data):
    try:
        # Connect to the database
        connection = sqlite3.connect('alsabeel_data.db')
        cursor = connection.cursor()
        # Delete records from the assistance table associated with the family
        cursor.execute("DELETE FROM assistance WHERE family_id=?", (family_id,))
        # Commit the changes
        connection.commit()
        # Close the cursor
        cursor.close()
        # Close the connection
        connection.close()
        insert_assistance_data(family_id, new_assistance_data)
        print("Children data updated successfully.")
    except Exception as e:
        print("An error occurred:", e)


@app.get("/", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("page1.html", {"request": request})
@app.get("/options", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("options.html", {"request": request})
@app.get("/page2", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("page2.html", {"request": request})
@app.get("/page3", response_class=HTMLResponse)
def page3(request: Request):
    status = Storage.status  # قيمة الحالة التي تريدها
    return templates.TemplateResponse("page3.html", {"request": request, "status": status})
@app.get("/page4", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("page4.html", {"request": request})
@app.get("/page5", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("page5.html", {"request": request})
@app.get("/page6", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("page6.html", {"request": request})
@app.post("/status")
async def endpoint(request: Request):
    data = await request.json()
    name = data["status"]
    Storage.status=name
    return name
@app.post("/send_data")
async def endpoint(request: Request):
    try:
        data = await request.json()
        d1=data['formData']['nationalNum']
        d2=data['formData']['nationalNum-w']
        if check_record_exists(d1) or check_record_exists(d2):
            return {"message":"السجل موجود!!!!!"}
        
        family_id = insert_family_data(data)
        children_data = data['formData']['childInfo']
        children_data=convert_dicts_to_tuples(children_data)
        insert_children_data(family_id, children_data)
        Storage.status=''
        return {"message": f"Data inserted successfully with family ID: {family_id}"}
    except Exception as e:
        return {"message":'Error: '+str(e)}

@app.get("/show_data_to_update")
async def endpoint(family_id:str,request: Request):
    try:
        family_data,children_data,assistance_data=display_family_record(family_id)
        children_list=[]
        assistance_list=[]
        family_info = {
        'husband': family_data[1],
        'father': family_data[2],
        'family': family_data[3],
        'birthday': family_data[4],
        'nationalNum': family_data[5],
        'job': family_data[6],
        'wife': family_data[7],
        'father-w': family_data[8],
        'family-w': family_data[9],
        'birthday-w': family_data[10],
        'nationalNum-w': family_data[11],
        'job-w': family_data[12],
        # Address information
        'state': family_data[13],
        'city': family_data[14],
        'village': family_data[15],
        'specificPoint': family_data[16],
        'house': family_data[17].lower(),
        'livingStatus': family_data[18],
        # Contact information
        'basicMobile': family_data[19],
        'alternativeMobile': family_data[20],
        'telephone': family_data[21],
        # Health information
        'familyHealth': family_data[22],
        'additionalInfo': family_data[23],
        # Data and input information
        'statusSource': family_data[24],
        'regDate': family_data[25],
        'applicant': family_data[26],
        'dataEntrier': family_data[27],
        'applicantEvaluation': family_data[28],
        'evaluationText': family_data[29],
        'managementNotes': family_data[30],
        'status': family_data[31],
        'status_1': family_data[32],
        'study_response': family_data[33],
        'income': family_data[34]
    }
        for child in children_data:
            child_info = {
            'child-name': child[0],
            'birthday-child': child[1],
            'study-work': child[2],
            'notes': child[3]}
            children_list.append(child_info)
        for help in assistance_data:
            help_info = {
            'help-value': help[0],
            'help-date': help[1]}
            assistance_list.append(help_info)

        result={'family':family_info,'childs':children_list,'helps':assistance_list}
        return result
    except:
        print ("No Data")

@app.get("/show_data_latest_help")
async def endpoint(request: Request):
    try:
        result=get_latest_assistance_info()
        return result
    except:
        print ("No Data")
@app.post("/show_data_latest_help_filter")
async def endpoint(request: Request):
    try:
        filters = await request.json()
        filters = filters['filters']
        if filters['status']=='الكل':
            filters.pop('status')
        for key, value in list(filters.items()):
            if len(str(value).strip()) ==0:
                filters.pop(key)
        try:
            family_id=filters['family_id']
            result=get_latest_assistance_info_with_family_id(family_id)
        except:
            result = get_latest_assistance_info_with_filter(filters)
        
        return result
    except Exception as e:
        print("No Data:", e)
@app.get("/delete_record")
async def endpoint(family_id,request: Request):
    try:
        delete_family_record(family_id)
    except:
        print ("No Record")
@app.post("/update_data")
async def endpoint(request: Request):
    data = await request.json()
    family_id_to_update=data['formData']['Family_id']
    new_family_data = (
    data['formData']['husband'], data['formData']['father'], data['formData']['family'],
        data['formData']['birthday'], data['formData']['nationalNum'], data['formData']['job'],
        data['formData']['wife'], data['formData']['father-w'], data['formData']['family-w'],
        data['formData']['birthday-w'], data['formData']['nationalNum-w'], data['formData']['job-w'],
        data['formData']['state'], data['formData']['city'], data['formData']['village'],
        data['formData']['specificPoint'], data['formData']['house'], data['formData']['livingStatus'],
        data['formData']['basicMobile'], data['formData']['alternativeMobile'], data['formData']['telephone'],
        data['formData']['familyHealth'], data['formData']['additionalInfo'], data['formData']['statusSource'],
        data['formData']['regDate'], data['formData']['applicant'], data['formData']['dataEntrier'],
        data['formData']['applicantEvaluation'], data['formData']['evaluationText'],
        data['formData']['managementNotes'],data['formData']['status'],
        data['formData']['status_1'],data['formData']['study_response'],data['formData']['income']
    )
    update_family_data(family_id_to_update, new_family_data)
    children_data = data['formData']['childInfo']
    new_children_data=convert_dicts_to_tuples(children_data)
    assistance_data = data['formData']['helpInfo']
    new_assistance_data=convert_dicts_to_tuples(assistance_data)
    update_children_data(family_id_to_update, new_children_data)
    update_assistance_data(family_id_to_update, new_assistance_data)
    print('ok')


    

    
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)