document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];
  if (!file) {
    alert("Please select a file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  // Show loading
  document.getElementById("loading").style.display = "block";
  document.getElementById("result").style.display = "none";

  try {
    const response = await fetch("/upload", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById("summaryText").textContent = data.summary;
      document.getElementById("actionItemsText").textContent = data.action_items.join("\n");
    } else {
      alert("Error: " + (data.error || "Something went wrong."));
    }

  } catch (error) {
    console.error("Error uploading file:", error);
    alert("Something went wrong. Check console for details.");
  } finally {
    document.getElementById("loading").style.display = "none";
    document.getElementById("result").style.display = "block";
  }
});
