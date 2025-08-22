from flask_restful import fields

from libs.helper import TimestampField

# Basic account fields for comment creators/resolvers
comment_account_fields = {"id": fields.String, "name": fields.String, "email": fields.String}

# Comment mention fields
workflow_comment_mention_fields = {
    "mentioned_user_id": fields.String,
    "mentioned_user_account": fields.Nested(comment_account_fields, allow_null=True),
}

# Comment reply fields
workflow_comment_reply_fields = {
    "id": fields.String,
    "content": fields.String,
    "created_by": fields.String,
    "created_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "created_at": TimestampField,
}

# Participant info for showing avatars
workflow_comment_participant_fields = {
    "id": fields.String,
    "name": fields.String,
    "email": fields.String,
    "avatar": fields.String,
}

# Basic comment fields (for list views)
workflow_comment_basic_fields = {
    "id": fields.String,
    "position_x": fields.Float,
    "position_y": fields.Float,
    "content": fields.String,
    "created_by": fields.String,
    "created_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "created_at": TimestampField,
    "updated_at": TimestampField,
    "resolved": fields.Boolean,
    "resolved_at": TimestampField,
    "resolved_by": fields.String,
    "resolved_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "reply_count": fields.Integer,
    "mention_count": fields.Integer,
    "participants": fields.List(fields.Nested(workflow_comment_participant_fields)),
}

# Detailed comment fields (for single comment view)
workflow_comment_detail_fields = {
    "id": fields.String,
    "position_x": fields.Float,
    "position_y": fields.Float,
    "content": fields.String,
    "created_by": fields.String,
    "created_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "created_at": TimestampField,
    "updated_at": TimestampField,
    "resolved": fields.Boolean,
    "resolved_at": TimestampField,
    "resolved_by": fields.String,
    "resolved_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "replies": fields.List(fields.Nested(workflow_comment_reply_fields)),
    "mentions": fields.List(fields.Nested(workflow_comment_mention_fields)),
}

# Comment creation response fields (simplified)
workflow_comment_create_fields = {
    "id": fields.String,
    "created_at": TimestampField,
}

# Comment update response fields
workflow_comment_update_fields = {
    "id": fields.String,
    "content": fields.String,
    "updated_at": TimestampField,
    "mentions": fields.List(fields.Nested(workflow_comment_mention_fields)),
}

# Comment resolve response fields
workflow_comment_resolve_fields = {
    "id": fields.String,
    "resolved": fields.Boolean,
    "resolved_at": TimestampField,
    "resolved_by": fields.String,
    "resolved_by_account": fields.Nested(comment_account_fields, allow_null=True),
}

# Comment pagination fields
workflow_comment_pagination_fields = {
    "data": fields.List(fields.Nested(workflow_comment_basic_fields), attribute="data"),
    "has_more": fields.Boolean,
    "total": fields.Integer,
    "page": fields.Integer,
    "limit": fields.Integer,
}

# Reply creation response fields
workflow_comment_reply_create_fields = {
    "id": fields.String,
    "content": fields.String,
    "created_by": fields.String,
    "created_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "created_at": TimestampField,
}

# Reply update response fields
workflow_comment_reply_update_fields = {
    "id": fields.String,
    "content": fields.String,
    "created_by": fields.String,
    "created_by_account": fields.Nested(comment_account_fields, allow_null=True),
    "created_at": TimestampField,
}
