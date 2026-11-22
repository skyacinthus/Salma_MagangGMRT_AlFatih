import math

base_h = 0.05
femur  = 0.4    
tibia  = 0.3     

deg1 = math.radians(float(input("joint_1: ")))
deg2 = math.radians(float(input("joint_2: ")))

z0 = base_h + femur           
r = tibia * math.cos(deg2)
z = z0 + tibia * math.sin(deg2)

x = r * math.cos(deg1) #rotasi around z
y = r * math.sin(deg1)

print("End effector")
print("x:", x)
print("y:", y)
print("z:", z)