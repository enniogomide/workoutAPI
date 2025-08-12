from fastapi import FastAPI

from routers import api_router

app = FastAPI(title='WorkoutApi')
app.include_router(api_router)


# if __name__ == 'main':
#     import uvicorn
# #    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info')
#     uvicorn.run('main:app', log_level='info')
#  uvicorn main:app --reload
