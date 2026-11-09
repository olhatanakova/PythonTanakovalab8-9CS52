import string
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import gutenberg, stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer

# Завантаження необхідних ресурсів NLTK
nltk.download("gutenberg")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

# 1. Завантаження тексту відповідно до варіанта 16
variant_file = "shakespeare-hamlet.txt"
text_words = gutenberg.words(variant_file)

print(f"Обраний текст: {variant_file}")

# 2. Визначення кількості слів та кількості унікальних слів
total_words = len(text_words)
unique_words = len(set(text_words))

print(f"\n--- 1. Кількість слів ---")
print(f"Загальна кількість слів у тексті: {total_words}")
print(f"Кількість унікальних слів у тексті: {unique_words}")
print(
    f"Порівняння: унікальні слова становлять приблизно {unique_words / total_words * 100:.2f}% від загальної кількості слів."
)

# 3. Визначення 10 найбільш уживаних слів у тексті та побудова діаграми
fdist = FreqDist(text_words)
top_ten_raw = fdist.most_common(10)
print(f"\n--- 2. 10 найбільш уживаних слів (з урахуванням стоп-слів та пунктуації) ---")
print(top_ten_raw)

# Побудова першої діаграми
words_raw, counts_raw = zip(*top_ten_raw)
plt.figure(figsize=(10, 5))
plt.bar(words_raw, counts_raw, color="skyblue")
plt.title(
    f"10 найбільш уживаних слів (до очищення) — {variant_file}", fontsize=12
)
plt.xlabel("Слова")
plt.ylabel("Частота")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Видалення стоп-слів та пунктуації
stop_words = set(stopwords.words("english"))
table = str.maketrans("", "", string.punctuation)

cleaned_words = [
    word.translate(table).lower()
    for word in text_words
    if word.translate(table) != ""
]
filtered_words = [
    word
    for word in cleaned_words
    if word not in stop_words and word.isalpha()
]

# Визначення 10 найбільш уживаних слів після очищення
fdist_filtered = FreqDist(filtered_words)
top_ten_filtered = fdist_filtered.most_common(10)
print(f"\n--- 3. 10 найбільш уживаних слів (після видалення стоп-слів та пунктуації) ---")
print(top_ten_filtered)

# Побудова другої діаграми
words_filt, counts_filt = zip(*top_ten_filtered)
plt.figure(figsize=(10, 5))
plt.bar(words_filt, counts_filt, color="salmon")
plt.title(
    f"10 найбільш уживаних слів (після очищення) — {variant_file}", fontsize=12
)
plt.xlabel("Слова")
plt.ylabel("Частота")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Лематизація слів і визначення 10 найбільш уживаних
lemmatizer = WordNetLemmatizer()
lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]

fdist_lemmatized = FreqDist(lemmatized_words)
top_ten_lemmatized = fdist_lemmatized.most_common(10)

print(f"\n--- 4. 10 найбільш уживаних слів після лематизації ---")
print(top_ten_lemmatized)
