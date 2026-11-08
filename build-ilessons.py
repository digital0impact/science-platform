#!/usr/bin/env python3
"""يولّد قسم «الدروس التفاعلية» في index.html من قسم المختبرات (LAB-BLOCK).
الشيفرة واحدة للقسمين؛ يتغير في النسخة: أسماء الدوال، والروابط، ونوع السجل kind، والنصوص الظاهرة."""
import re, sys
path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
s = open(path, encoding="utf-8").read()
a = s.index("/*<LAB-BLOCK>"); a = s.index("*/", a) + 2
b = s.index("/*</LAB-BLOCK>*/")
block = s[a:b]

# 1) أمثلة خاصة بالمختبر تُستبدل بأمثلة للدرس التفاعلي (قبل الاستبدال العام)
special = [
  (r'placeholder="مثال: مختبر أنواع الصخور"', 'placeholder="مثال: دورة الصخور خطوة بخطوة"'),
  (r'placeholder="مثال: مختبر تفرز[^"]*"', 'placeholder="مثال: درس تفاعلي عن دورة الصخور: يبدأ بسؤال مشوّق، ثم خطوة قصيرة لكل نوع من الصخور مع رسم يتغير عند الضغط، ثم نشاط ترتيب مراحل الدورة بالسحب، وسؤال سريع بعد كل خطوة، وملخص في النهاية."'),
  (r'placeholder="مثال: كبّري العينات[^"]*"', 'placeholder="مثال: اختصري الشرح في الخطوة الثانية، وكبّري الرسم، وأضيفي سؤالاً سريعاً بعد الخطوة الأخيرة."'),
  (r'جرّبي واكتشفي بنفسك', 'تعلّمي خطوة بخطوة'),
  (r'أنجزتِ مختبر', 'أنجزتِ الدرس التفاعلي'),
  (r'ما تريدين أن تجرّبه الطالبة', 'ما تريدين أن تتعلمه الطالبة وكيف تتفاعل معه'),
  (r'«المختبرات»', '«الدروس التفاعلية»'),
  (r'" · داخل المختبر"', '" · اختبار الصفحة"'),
]
for pat, rep in special: block = re.sub(pat, rep, block)

# 2) أسماء الدوال والحالة (لا تمس Store.saveLab وأمثالها)
idents = [("viewLabEditor","viewILessonEditor"),("viewLabs","viewILessons"),("viewLab","viewILesson"),
          ("drawLabQuiz","drawILQuiz"),("drawLabQs","drawILQs"),("generateLabQuestions","generateILQuestions"),
          ("drawLabPreview","drawILPreview"),("runLabAI","runILAI"),("saveLab","saveIL"),("LB","IL"),("READY_LABS","READY_ILESSONS")]
for old, new in idents: block = re.sub(r'(?<![.\w])' + old + r'\b', new, block)

# 3) الروابط ونوع السجل والتنسيق
for old, new in [('#labedit=', '#iledit='), ('#lab=', '#ilesson='), ('href="#labs"', 'href="#ilessons"'),
                 ('location.hash = "labs"', 'location.hash = "ilessons"'),
                 ('=== "lab")', '=== "interactive")'), ('kind: "lab"', 'kind: "interactive"'),
                 ('chip lab"', 'chip ilesson"')]:
    block = block.replace(old, new)

# 4) النصوص الظاهرة (الأطول أولاً)
for old, new in [("مختبرات لبيبة الجاهزة","دروس لبيبة التفاعلية الجاهزة"),("مختبر افتراضي","درس تفاعلي"),
                 ("المختبرات الافتراضية","الدروس التفاعلية"),("المختبرات","الدروس التفاعلية"),("مختبرات","دروس تفاعلية"),
                 ("مختبراً","درساً تفاعلياً"),("المختبر","الدرس التفاعلي"),("مختبر","درس تفاعلي")]:
    block = block.replace(old, new)

c = s.index("/*<ILESSON-BLOCK>*/") + len("/*<ILESSON-BLOCK>*/")
d = s.index("/*</ILESSON-BLOCK>*/")
s = s[:c] + "\n/* مولَّد آلياً من LAB-BLOCK بالسكربت build-ilessons.py — لا تعدّليه يدوياً */" + block + s[d:]
open(path, "w", encoding="utf-8").write(s)
print("interactive block:", len(block), "chars")
