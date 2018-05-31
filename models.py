from orm import Structure, String, Integer, Float


class Stock(Structure):
    name = String()
    shares = Integer()
    price = Float()