from django import template

register = template.Library()

@register.filter
def translate_status(value):
    translations = {
        'requested': 'قيد الطلب',
        'approved': 'تمت الموافقة',
        'completed': 'مكتمل',
        'cancelled': 'ملغى',
    }
    return translations.get(value.lower(), value)
