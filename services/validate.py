def check_amount(amount):
  if int(amount) < 0:
    raise Error("Amount can't have a negative value")