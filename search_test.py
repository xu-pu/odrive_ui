import odrive

my_drive = odrive.find_any(find_multiple=2)
print(type(my_drive))
print(len(my_drive))