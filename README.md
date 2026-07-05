# Skillary

Демонстрационный сайт онлайн-школы: каталог программ, фильтрация по уровню, варианты оплаты, FAQ и передача заявки разработчику в Telegram.

## Возможности

- адаптивный редакционный дизайн;
- фильтры курсов и интерактивные тарифы;
- доступный FAQ с `aria-expanded`;
- честный переход в Telegram без имитации отправки формы.

Стек: HTML5, CSS, vanilla JavaScript, pytest. Это демонстрационный проект, компания и предложения вымышлены.

## Локальный запуск и проверка

```bash
(cd portfolio-packaging/skillary && python3 -m http.server 8000)
pytest portfolio-packaging/skillary/tests/test_site.py -v
PYTHONPATH=portfolio-packaging python3 portfolio-packaging/scripts/check_static_site.py portfolio-packaging/skillary
node --check portfolio-packaging/skillary/assets/js/main.js
```

После публикации: `https://brtvd07.github.io/skillary/`.
