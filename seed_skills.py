import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from exchange.models import Skill

initial_skills = [
    ("برمجة بايثون", "تعلم كيفية البرمجة باستخدام لغة بايثون، من الأساسيات إلى المفاهيم المتقدمة."),
    ("التصميم الجرافيكي", "أتقن أدوات مثل فوتوشوب وفيجما لإنشاء تصاميم مذهلة."),
    ("الرياضيات", "احصل على مساعدة في حساب التفاضل والتكامل، والجبر، أو الإحصاء."),
    ("اللغة الإسبانية", "تعلم التحدث والقراءة والكتابة باللغة الإسبانية."),
    ("تطوير الويب", "قم ببناء مواقع ويب حديثة باستخدام HTML وCSS وJavaScript."),
    ("التصوير الفوتوغرافي", "تعلم فن التقاط صور رائعة ومعالجتها."),
    ("التسويق الرقمي", "افهم تحسين محركات البحث، والتسويق عبر وسائل التواصل الاجتماعي، وحملات الإعلانات."),
    ("التحدث أمام الجمهور", "حسن مهاراتك في التواصل والتقديم."),
]

def populate():
    print("Populating initial skills...")
    for name, desc in initial_skills:
        skill, created = Skill.objects.get_or_create(name=name, defaults={'description': desc})
        if created:
            print(f"Created skill: {name}")
        else:
            print(f"Skill already exists: {name}")
    print("Done!")

if __name__ == '__main__':
    populate()
