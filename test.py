from transliterate import translit, slugify
import re


class Post:
    title = "Руководство по Python для начинающих"
    content = """Python - это высокоуровневый язык программирования,
                 который отлично подходит для начинающих разработчиков.
                 В этой статье мы рассмотрим основы языка..."""
    category = 2,
    status = "PUBLISHED"

res = translit(Post.content, "ru", reversed=True)
res = res.lower().replace("'", "").replace('"', '').replace(" ", "-")
res = re.sub("-+", "-", res)

print(res)