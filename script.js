document.getElementById("convertBtn").addEventListener("click", async () => {
  const videoURL = document.getElementById("videoURL").value;
  const resultDiv = document.getElementById("result");
  const convertBtn = document.getElementById("convertBtn");

  if (!videoURL) {
    resultDiv.innerText = "Please enter a YouTube URL!";
    return;
  }

  // Disable button and show loading message
  convertBtn.disabled = true;
  resultDiv.innerText = "Conversion started! Please wait...";

  try {
    let abac = "http://127.0.0.1:5000/convert";
    const response = await fetch(abac, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: videoURL }),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Server response:", data, "Status:", response.status);
      throw new Error(data.error || `Conversion failed (Status: ${response.status})`);
    }

    // Update result div and start download
    resultDiv.innerText = " ✅ Downloaded";
    const filename = data.filename;
    const downloadUrl = `http://127.0.0.1:5000/download/${filename}`;

    const a = document.createElement("a");
    a.style.display = "none";
    a.href = downloadUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

  } catch (error) {
    console.error("Full error:", error);
    resultDiv.innerText = "❌ Error: " + error.message;
  } finally {
    // Re-enable button
    convertBtn.disabled = false;
  }
});