document.addEventListener("DOMContentLoaded", function () {
  const messages = document.querySelectorAll('[id^="message-"]');
  messages.forEach((message) => {
    setTimeout(() => {
      message.style.transition =
        "opacity 0.5s ease-in-out, transform 0.5s ease-in-out";
      message.style.opacity = "0";
      message.style.transform = "translateY(20px)";
      setTimeout(() => {
        message.remove();
      }, 500);
    }, 3000);
  });
});
