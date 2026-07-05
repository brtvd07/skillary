const filters = document.querySelectorAll(".filter-btn");
const courses = document.querySelectorAll(".course-card");
let selectedCourse = "";
let selectedTariff = "Помесячно";

const updateLeadContext = () => {
  const courseText = selectedCourse ? `Курс: ${selectedCourse}. ` : "Курс можно выбрать в каталоге. ";
  document.querySelector("#lead-context").textContent = `${courseText}Тариф: ${selectedTariff}.`;
};

filters.forEach((button) => {
  button.addEventListener("click", () => {
    filters.forEach((item) => {
      item.classList.remove("active");
      item.setAttribute("aria-pressed", String(item === button));
    });
    button.classList.add("active");
    courses.forEach((course) => {
      course.hidden = button.dataset.level !== "all" && course.dataset.level !== button.dataset.level;
    });
  });
});

document.querySelectorAll(".course-choice").forEach((link) => {
  link.addEventListener("click", () => {
    selectedCourse = link.dataset.course;
    updateLeadContext();
  });
});

const tariffs = {
  monthly: { price: "2 490 ₽", note: "в месяц, доступ к текущему модулю", saving: false },
  full: { price: "19 900 ₽", note: "за весь курс, доступ ко всем модулям", saving: true },
};

document.querySelectorAll(".tariff-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const tariff = tariffs[button.dataset.mode];
    document.querySelectorAll(".tariff-toggle").forEach((item) => {
      item.classList.toggle("active", item === button);
      item.setAttribute("aria-pressed", String(item === button));
    });
    selectedTariff = button.textContent.trim();
    document.querySelector("#price-value").textContent = tariff.price;
    document.querySelector("#price-note").textContent = tariff.note;
    document.querySelector("#saving").hidden = !tariff.saving;
    updateLeadContext();
  });
});

document.querySelectorAll(".faq-question").forEach((button) => {
  button.addEventListener("click", () => {
    const isOpen = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!isOpen));
    document.getElementById(button.getAttribute("aria-controls")).hidden = isOpen;
  });
});

document.querySelector("#lead-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const name = new FormData(event.currentTarget).get("name").trim();
  const courseDetails = selectedCourse ? ` Курс: ${selectedCourse}.` : "";
  const message = `Здравствуйте! Хочу обсудить сайт онлайн-школы по примеру Skillary. Имя: ${name}.${courseDetails} Тариф: ${selectedTariff}.`;
  window.location.href = "https://t.me/brtvd_07?text=" + encodeURIComponent(message);
});
