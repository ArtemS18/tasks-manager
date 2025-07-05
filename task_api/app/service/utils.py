import functools
import logging
from time import perf_counter
from typing import Callable
from fastapi import Response

def set_cookie(
        response:Response,
        key: str,
        value: str,
        httponly=True,      
        secure=False,          
        samesite="lax",       
        max_age=60 * 60 * 24,  
        path="/"
    ):
    response.set_cookie(
        key=key,
        value=value,
        httponly=httponly,      
        secure=secure,          
        samesite=samesite,       
        max_age=max_age,  
        path=path
    )
    return response

