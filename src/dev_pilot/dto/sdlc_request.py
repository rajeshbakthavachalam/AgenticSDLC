from pydantic import BaseModel, Field
from typing import Optional

class SDLCRequest(BaseModel):
    project_name: str = Field(..., 
                              example="Ecommerce Platform",
                              description="The name of the project")
    requirements: Optional[list[str]] = Field(None, 
                                                example=["Users can browser the products", 
                                                         "Users should be able to add the product in the cart",
                                                         "Users should be able to do the payment",
                                                         "Users should be able to see their order history"],
                                                description="The list of requirements for the project")