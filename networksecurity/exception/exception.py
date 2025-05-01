import sys
print(sys.path)
sys.path.append(r'E:\ML projects\fastapi\networksecurity')
from networksecurity.logger.logger import logger

class NetworksecurityException(Exception):
    def __init__(self,error_message,error_detail:sys):
        self.error_message=error_message
        _,_,exc_tb=error_detail.exc_info()
        
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename
    
    def _str_(self):
        return"Error occured in python script name [{0}] line number [{1}] error message[{2}]"
        self.filename,self.lineno,str(self.error_message)

if __name__=="__main__":
    try:
        logger.info("enterthe try block")
        a=1/0
        print("this will be not printed")
    except Exception as e:
        raise NetworksecurityException(e,sys)



        