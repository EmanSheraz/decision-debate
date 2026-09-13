const API_URL = "http://localhost:8000";

const startBtn = document.getElementById("startBtn");
const input = document.getElementById("decisionInput");
const chat = document.getElementById("chat");
const verdictBox = document.getElementById("verdict");

startBtn.addEventListener("click", startDebate);
input.addEventListener("keydown", (e) => e.key === "Enter" && startDebate());

async function startDebate() {
  const decision = input.value.trim();
  if (!decision) return;

  chat.innerHTML = "";
  verdictBox.classList.remove("show");
  verdictBox.classList.add("hidden");
  startBtn.disabled = true;
  startBtn.textContent = "Debating...";

  try {
    const res = await fetch(`${API_URL}/debate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ decision, rounds: 3 }),
    });
    const data = await res.json();
    await revealTranscript(data.transcript);
    showVerdict(data.verdict);
  } catch (err) {
    chat.innerHTML = `<p class="error-msg">Error: ${err.message}. Is the backend running?</p>`;
  } finally {
    startBtn.disabled = false;
    startBtn.textContent = "Start Debate";
  }
}

function revealTurn(turn) {
  return new Promise((resolve) => {
    const entry = document.createElement("div");
    entry.className = `turn ${turn.speaker.toLowerCase()}`;
    const name = turn.speaker === "FOR" ? "The Optimist" : "The Skeptic";
    entry.innerHTML = `<div class="speaker">${name}</div><div class="text">${turn.text}</div>`;
    chat.appendChild(entry);
    setTimeout(resolve, 900);
  });
}

async function revealTranscript(transcript) {
  for (const turn of transcript) {
    await revealTurn(turn);
  }
}

function showVerdict(text) {
  verdictBox.innerHTML = `<div class="title">The Judge's Verdict</div><div class="text">${text}</div>`;
  verdictBox.classList.remove("hidden");
  // trigger the seal animation on next frame
  requestAnimationFrame(() => verdictBox.classList.add("show"));
}