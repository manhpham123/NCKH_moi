from fastapi import FastAPI
#from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.encoders import jsonable_encoder
from data import *
import pandas as pd
import json
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import pandas as pd
import uvicorn
from model import *
from typing import List, Dict
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import paramiko



app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["cici_flow"]

ip = "192.168.189.133"
intf_str = "ens33"
num_rows = 0

collection = db[f"flow_data_{ip}_{intf_str}"]

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Danh sách các nguồn gốc có thể truy cập API của bạn
    allow_credentials=True,
    allow_methods=["*"], # Phương thức HTTP cho phép
    allow_headers=["*"], # Tiêu đề HTTP cho phép
)

# @app.get("/items/", response_model=List[dict])
# async def read_items():
#     try:
    
        
#         # # Tiền xử lý dữ liệu
#         # df_processed = preprocess_flow(df_f)
        
#         # # Dự đoán
#         # pred = model.predict(df_processed)
        
#         # # Thêm kết quả dự đoán vào DataFrame
#         # df_f['label'] = pred
        
#         df_l = predict_label(collection)

        
#         return df_l[0:15]
        
#         # Trả về kết quả dưới dạng JSON
#         #return df_f.to_dict(orient='records')
#     except Exception as e:
#     # Nếu có lỗi, trả về thông báo lỗi với status code 500
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import paramiko
# Thay thế các thông tin dưới đây với thông tin thực tế của bạn
# host = '192.168.189.133'
# port = 22  # Port SSH mặc định
# username = 'william'
# password = 'k'
# command = '/home/william/Desktop/run_command.sh'  # Lệnh bạn muốn thực thi




# @app.post("/control/on")
# def execute_ssh_sudo_command_api(ip: str = Query(1, alias="ip")):
#     execute_ssh_sudo_command(host, port, username, password, command)
    

    
  
    
#API: http://127.0.0.1:8000/items/?page=1&limit=10&filter_field=Source%20IP&filter_value=117.18.232.200   
@app.get("/items/", response_model=Dict)
async def read_items(page: int = Query(1, alias="page"), limit: int = Query(1, alias="limit"), filter_field: str = Query("", alias="filter_field"), filter_value: str = Query("", alias="filter_value")):
    try:
        if (filter_field == "") | (filter_value == ""):
            skip = (page - 1) * limit
            # Tiền xử lý và dự đoán ở đây
            df_l, df_st = predict_label(collection)
            
            total = len(df_st)
            
            limit = limit
            
            page = page
            
            # Áp dụng phân trang
            paginated_items = df_st[skip : skip + limit]
            
            re_ob = {
                "data": paginated_items,
                "limit": limit,
                "page": page,
                "total": total
            }
            
            # Trả về kết quả dưới dạng JSON
            return re_ob
        else :
            skip = (page - 1) * limit
            # Tiền xử lý và dự đoán ở đây
            df_l, df_st = predict_label(collection)
            
            df_st = Filter(filter_field, filter_value, df_st)
            
            total = len(df_st)
            
            limit = limit
            
            page = page
            
            # Áp dụng phân trang
            paginated_items = df_st[skip : skip + limit]
            
            re_ob = {
                "data": paginated_items,
                "limit": limit,
                "page": page,
                "total": total
            }
            
            return re_ob
            
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/alert/", response_model=Dict)
async def read_alert(page: int = Query(1, alias="page"), limit: int = Query(1, alias="limit")):
    try:
        
        skip = (page - 1) * limit
        # Tiền xử lý và dự đoán ở đây
        #df_l, df_st = predict_label(collection)
        
        df_p, df_st = predict_label(collection)
        
        
        df_a = get_alert(df_st)
        
        
        total = len(df_a)
        
        limit = limit
        
        page = page
        
        # Áp dụng phân trang
        paginated_items = df_a[skip : skip + limit]
        
        re_ob = {
            "data": paginated_items,
            "limit": limit,
            "page": page,
            "total": total
        }
        
        # Trả về kết quả dưới dạng JSON
        return re_ob
    except Exception as e:
        # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/alert/", response_model=List[dict])
# async def read_alert():
#     try:
        
#         df_l, df_st = predict_label(collection)
#         df_a = get_alert(df_st)

        
#         return df_a[-100:]
        
#         # Trả về kết quả dưới dạng JSON
#         #return df_f.to_dict(orient='records')
#     except Exception as e:
#     # Nếu có lỗi, trả về thông báo lỗi với status code 500
#         raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/statc/protocol", response_model=Dict)
async def static_protocol():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_pro_ls = dict(sorted(static_data.pro_ls.items(), key=lambda x:x[1], reverse=True))
        
       
        return sorted_pro_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/statc/flow", response_model=Dict)
async def static_protocol():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_flw_ls = dict(sorted(static_data.ip_ls.items(), key=lambda x:x[1], reverse=True))
        
        
        return sorted_flw_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
#API: http://127.0.0.1:8000/statc/service
@app.get("/statc/service", response_model=Dict)
async def static_protocol():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_ser_ls = dict(sorted(static_data.service_ls.items(), key=lambda x:x[1], reverse=True))
        
        return sorted_ser_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.get("/statc/attack", response_model=Dict)
async def static_attack():
    try:
        df_l, df_st = predict_label(collection)
        
        static_data = get_ls(df_st)
        
        sorted_att_ls = dict(sorted(static_data.alert_ls.items(), key=lambda x:x[1], reverse=True))
       
        return sorted_att_ls
        
        # Trả về kết quả dưới dạng JSON
        #return df_f.to_dict(orient='records')
    except Exception as e:
    # Nếu có lỗi, trả về thông báo lỗi với status code 500
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
