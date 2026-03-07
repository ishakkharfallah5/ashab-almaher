import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exchange.models import Skill

translations = {
    "Python Programming": ("برمجة بايثون", "تعلم كيفية البرمجة باستخدام لغة بايثون، من الأساسيات إلى المفاهيم المتقدمة."),
    "Graphic Design": ("التصميم الجرافيكي", "أتقن أدوات مثل فوتوشوب وفيجما لإنشاء تصاميم مذهلة."),
    "Mathematics": ("الرياضيات", "احصل على مساعدة في حساب التفاضل والتكامل، والجبر، أو الإحصاء."),
    "Spanish Language": ("اللغة الإسبانية", "تعلم التحدث والقراءة والكتابة باللغة الإسبانية."),
    "Web Development": ("تطوير الويب", "قم ببناء مواقع ويب حديثة باستخدام HTML وCSS وJavaScript."),
    "Photography": ("التصوير الفوتوغرافي", "تعلم فن التقاط صور رائعة ومعالجتها."),
    "Digital Marketing": ("التسويق الرقمي", "افهم تحسين محركات البحث، والتسويق عبر وسائل التواصل الاجتماعي، وحملات الإعلانات."),
    "Public Speaking": ("التحدث أمام الجمهور", "حسن مهاراتك في التواصل والتقديم."),
}

def translate():
    print("Translating skills in database...")
    for old_name, (new_name, new_desc) in translations.items():
        try:
            skill = Skill.objects.get(name=old_name)
            skill.name = new_name
            skill.description = new_desc
            skill.save()
            print(f"Translated: {old_name} -> {new_name}")
        except Skill.DoesNotExist:
            print(f"Skill not found: {old_name}")
    print("Done!")

if __name__ == '__main__':
    translate()
