from marshmallow import Schema, fields, validate


# For registration
class UserSchema(Schema):
    # id = fields.Int(dump_only=True)
    email = fields.Email(required=True, error_messages={"required": "Email is required"})
    password = fields.Str(required=True, load_only=True, error_messages={"required": "Password is required"})
    first_name = fields.Str(required=True, error_messages={"required": "First name is required"})
    last_name = fields.Str(required=True, error_messages={"required": "Last name is required"})
    middle_name = fields.Str(required=True, error_messages={"required": "Middle name is required"})
    student_id = fields.Str(required=True, error_messages={"required": "Student ID is required"})
    department = fields.Str(required=True, error_messages={"required": "Department is required"})
    status = fields.Str(required=True, error_messages={"required": "Status is required"})

# For login
class LoginSchema(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required"})
    password = fields.Str(required=True, load_only=True, error_messages={"required": "Password is required"})

# For Not Verified Users
class ForVerification(Schema):
    email = fields.Email(required=True, error_messages={"required": "Email is required"})
    token = fields.Str(required=True, error_messages={"required": "Token is required"})
    isVerified = fields.Bool(required=True, error_messages={"required": "Verification status is required"})