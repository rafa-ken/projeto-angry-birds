import math

def vec_add(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

def vec_sub(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1]]

def vec_scale(v, scalar):
    return [v[0] * scalar, v[1] * scalar]

def vec_rotate(v, angle_degrees):
    angle_radians = math.radians(angle_degrees)
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    return [
        v[0] * cos_angle - v[1] * sin_angle,
        v[0] * sin_angle + v[1] * cos_angle
    ]

def vec_length(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def vec_normalize(v):
    length = vec_length(v)
    if length == 0:
        return [0, 0]
    return [v[0] / length, v[1] / length]

def vec_dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]
