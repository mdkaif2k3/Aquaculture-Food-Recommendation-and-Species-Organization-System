document.addEventListener("DOMContentLoaded", () => {
  console.log("Scroll fade JS loaded");
  const elements = document.querySelectorAll(".fadeup");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show"); 
        } else {
          entry.target.classList.remove("show"); 
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -20px 0px"
    }
  );

  elements.forEach(el => observer.observe(el));
});
