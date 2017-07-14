from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_uri = "postgresql://u:p@host/database" 
engine = create_engine(db_uri, echo=True)
Base = declarative_base(engine)
########################################################################
class Places(Base):
    """"""
    __tablename__ = 'temp_batch_insurance0_t'
 
    cust_id = Column(Integer)
    seqnum = Column(Integer, primary_key=True)
    treatment_code = Column(String)
    cpi = Column(String)
    acctnum = Column(String)
    acctnum_seq = Column(Integer)
    hid = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, cust_id, seqnum, treatment_code, cpi, acctnum,
                 acctnum_seq, hid):
        """"""
        self.cust_id = cust_id
        self.seqnum = seqnum
        self.treatment_code = treatment_code
        self.cpi = cpi
        self.acctnum = acctnum
        self.acctnum_seq = acctnum_seq
        self.hid = hid
 
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<Places - '%s': '%s' - '%s'>" % (self.cust_id, self.seqnum,
                                                 self.hid)
 
#----------------------------------------------------------------------
def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
if __name__ == "__main__":
    session = loadSession()
    res = session.query(Places).all()
    for i in range(10):
        print('{}, {}'.format(res[i].cust_id, res[i].seqnum))