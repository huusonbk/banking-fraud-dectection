from pydantic import BaseModel


# Type hint for attributes of a house
class TransactionInfo(BaseModel):
    step: int = 208
    type: str = "TRANSFER"
    amount: float = 256440.86
    nameOrig: str = "C1001269496"
    oldbalanceOrg: float = 554.0
    newbalanceOrig: float = 256994.86
    nameDest: str = "C1503528288"
    oldbalanceDest: float = 0.0
    newbalanceDest: float = 0.0


# Type hint for all the predictions of a house
class TransactionPrediction(BaseModel):
    Fraud: int
