from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))


def parsed_site():
    parser = SiteParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser


def test_course_filters_cover_all_levels():
    parser = parsed_site()
    levels = {
        attrs.get("data-level")
        for tag, attrs in parser.elements
        if tag == "button" and "filter-btn" in attrs.get("class", "")
    }
    assert levels == {"all", "beginner", "middle", "advanced"}
    filter_controls = [
        attrs
        for tag, attrs in parser.elements
        if tag == "button" and "filter-btn" in attrs.get("class", "")
    ]
    assert [item.get("aria-pressed") for item in filter_controls] == [
        "true", "false", "false", "false"
    ]


def test_tariff_modes_are_explicit_buttons():
    parser = parsed_site()
    modes = {
        attrs.get("data-mode")
        for tag, attrs in parser.elements
        if tag == "button" and "tariff-toggle" in attrs.get("class", "")
    }
    assert modes == {"monthly", "full"}
    tariff_controls = [
        attrs
        for tag, attrs in parser.elements
        if tag == "button" and "tariff-toggle" in attrs.get("class", "")
    ]
    assert [item.get("aria-pressed") for item in tariff_controls] == ["true", "false"]


def test_faq_controls_expose_expanded_state():
    parser = parsed_site()
    controls = [
        attrs
        for tag, attrs in parser.elements
        if tag == "button" and "faq-question" in attrs.get("class", "")
    ]
    assert len(controls) >= 3
    assert all(item.get("aria-expanded") == "false" for item in controls)
    assert all(item.get("aria-controls") for item in controls)


def test_signup_hands_off_to_telegram():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    javascript = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
    assert 'href="https://t.me/brtvd_07"' in html
    assert 'window.location.href = "https://t.me/brtvd_07?text=" + encodeURIComponent(message)' in javascript
    assert "Спасибо! Урок отправлен" not in html + javascript


def test_course_and_tariff_selection_flow_into_telegram_draft():
    parser = parsed_site()
    course_links = [
        attrs
        for tag, attrs in parser.elements
        if tag == "a" and "course-choice" in attrs.get("class", "")
    ]
    assert len(course_links) == 6
    assert all(item.get("data-course") for item in course_links)
    assert all(item.get("href") == "#contact" for item in course_links)

    javascript = (ROOT / "assets/js/main.js").read_text(encoding="utf-8")
    assert 'let selectedCourse = ""' in javascript
    assert 'let selectedTariff = "Помесячно"' in javascript
    assert "selectedCourse = link.dataset.course" in javascript
    assert "selectedTariff = button.textContent.trim()" in javascript
    assert "Имя: ${name}" in javascript
    assert "Курс: ${selectedCourse}" in javascript
    assert "Тариф: ${selectedTariff}" in javascript
    assert 'setAttribute("aria-pressed"' in javascript


def test_plan_disclaimer_and_public_url_are_exact():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Демонстрационный проект — компания вымышлена" in html
    assert "https://brtvd07.github.io/skillary/" in readme
