from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

''' Use declarative autoload method by SQLAlchemy '''
db_uri = "postgresql://u:p@host/database"
engine = create_engine(db_uri, echo=True)
Base = declarative_base(engine)
########################################################################
class TempBatchInsurance0(Base):
    """"""
    __tablename__ = 'temp_batch_insurance0_t'
    __table_args__ = {'autoload':True}
 
#----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
if __name__ == "__main__":
    session = loadSession()
    res = session.query(TempBatchInsurance0).all()
    print(res[1].cust_id)