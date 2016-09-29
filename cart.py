def _lfilter(f, i):
  return list(filter(f, i))

def get_cart(session):
  return session.get('cart', [])

def filter_by_pid(pid, cart):
  return _lfilter(lambda l: l['pid'] == pid, cart)

def filter_by_not_pid(pid, cart):
  return _lfilter(lambda l: l['pid'] != pid, cart)

def purge_empty(cart):
  purged = _lfilter(lambda l: l['qty'] >= 1, cart)
  return purged

def sort_by_pid(cart, reverse=False):
  return sorted(cart, key=lambda l: l['pid'], reverse=reverse)

def sort_by_qty(cart, reverse=False):
  return sorted(cart, key=lambda l: l['qty'], reverse=reverse)

def cart_eq(c1, c2):
  return sort_by_pid(c2) == sort_by_pid(c2)

def make_line(pid, qty):
  return { 'pid' : pid
         , 'qty' : qty
         , 'opt' : []
         }

def update_line_qty(pid, new_qty, cart):
  tmp_cart = filter_by_not_pid(pid, cart)
  if new_qty <= 0:
    return tmp_cart
  return tmp_cart + [make_line(pid, new_qty)]

def add_to_line_qty(pid, amt, cart):
  old_line = filter_by_pid(pid, cart)
  if old_line:
    old_qty = old_line[0]['qty'] 
  else:
    old_qty = 0
  return update_line_qty(pid, (amt + old_qty), cart)

def sub_from_line_qty(pid, amt, cart):
  return add_to_line_qty(pid, (-amt), cart)
