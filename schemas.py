from pydantic import BaseModel,Field,EmailStr,ConfigDict
class UserRegistrationDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name:str = Field(min_length=2,max_length=30)
    age:int = Field(ge=1)
    email:EmailStr
    password:str
class LoginUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email:EmailStr
    password:str
class AddBookDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title:str
    description:str
    read_url:str
class ReadBookDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str
class ReadBooknDescDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title:str
    description:str
    read_url:str
class ReadUserAdminDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name:str
    age:int
    email:EmailStr
    role:str
class ReadUserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name:str
    age:int
    books:list[ReadBookDTO]
class ReadUserMeDTO(ReadUserAdminDTO):
    pass
    


    
