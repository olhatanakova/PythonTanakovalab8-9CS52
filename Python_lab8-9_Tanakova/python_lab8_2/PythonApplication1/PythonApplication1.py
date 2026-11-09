import matplotlib.pyplot as plt
import pandas as pd

# Налаштування стилю та розміру графіків
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

# 1. Завантаження даних
df = pd.read_csv('comptagevelo20152.csv', sep=',', encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')

# 2. Фільтрація даних за 2015 рік (варіант 16)
df_2015 = df[df.index.year == 2015]

print('--- ПЕРВИННИЙ АНАЛІЗ ДАНИХ (head) ---')
print(df_2015.head())

print('\n--- ІНФОРМАЦІЯ ПРО DATAFRAME (info) ---')
print(df_2015.info())

print('\n--- СТАТИСТИЧНИЙ ОПИС (describe) ---')
print(df_2015.describe())

# 3. ОБРОБКА ДАНИХ

# А) Загальна кількість велосипедистів за 2015 рік для всіх велодоріжок
total_cyclists = df_2015.sum().sum()
print(
    f'\nЗагальна кількість велосипедистів за 2015 рік: {total_cyclists:,.0f}'
)

# Б) Найбільш популярний місяць для трьох обраних велодоріжок
# Перевірте точні назви стовпців через print(df_2015.columns) якщо буде помилка
selected_tracks = ['Maisonneuve_2', 'Brebeuf', 'Berri']
monthly_tracks = df_2015[selected_tracks].groupby(
    df_2015[selected_tracks].index.month
).sum()

print('\nНайбільш популярні місяці для обраних велодоріжок:')
for track in selected_tracks:
  if track in monthly_tracks.columns:
    best_month = monthly_tracks[track].idxmax()
    max_val = monthly_tracks[track].max()
    print(f'- {track}: місяць №{best_month} (усього: {max_val:,.0f} поїздок)')

# В) Групування даних за місяцями та визначення динаміки однієї велодоріжки
track_name = 'Maisonneuve_2'
if track_name in df_2015.columns:
  monthly_dynamics = df_2015[track_name].groupby(df_2015.index.month).sum()
  print(f'\nДинаміка використання велодоріжки {track_name} за місяцями:')
  print(monthly_dynamics)

  # 4. ПОБУДУВАННЯ ГРАФІКА
  monthly_dynamics.plot(
      kind='line',
      marker='o',
      color='b',
      linewidth=2,
      markersize=8,
  )
  plt.title(
      f'Динаміка використання велодоріжки {track_name} у 2015 році за місяцями',
      fontsize=14,
  )
  plt.xlabel('Місяць', fontsize=12)
  plt.ylabel('Кількість велосипедистів', fontsize=12)
  plt.grid(True)
  plt.xticks(
      range(1, 13),
      [
          'Січ',
          'Лют',
          'Бер',
          'Кві',
          'Тра',
          'Чер',
          'Лип',
          'Сер',
          'Вер',
          'Жов',
          'Лис',
          'Гру',
      ],
  )
  plt.show()