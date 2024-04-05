from marshmallow import Schema, fields

class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    is_completed = fields.Bool(required=True)

class TaskSchema(PlainTaskSchema):
    title = fields.Str()
    is_completed = fields.Bool()

class AddTaskSchema(Schema):
    title = fields.Str(required=True)
    is_completed = fields.Bool(required=True)

class BunchSchemaForAdd(Schema):
    tasks = fields.List(fields.Nested(AddTaskSchema))

class TaskIdSchema(Schema):
    id = fields.Int(required=True)

class BunchSchema(Schema):
    tasks = fields.List(fields.Nested(TaskIdSchema))