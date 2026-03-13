document.addEventListener("DOMContentLoaded", () => {
  const leftPanel = document.querySelector(".left-panel");
  const refreshButton = document.querySelector(".btn");
  const selectAllButton = document.querySelector(".btn.green");

  let matches = [];
  let allSelected = false;

  async function loadTodayMatches() {
    removeOldMatchList();
    showLoading();

    try {
      const response = await fetch("/today-matches");
      const data = await response.json();

      matches = normalizeMatches(data);

      removeOldMatchList();

      if (!matches.length) {
        showEmpty();
        return;
      }

      renderMatches(matches);
    } catch (error) {
      console.error("Maçlar yüklenemedi:", error);
      removeOldMatchList();
      showError();
    }
  }

  function normalizeMatches(data) {
    if (Array.isArray(data)) return data;
    if (Array.isArray(data.matches)) return data.matches;
    if (Array.isArray(data.data)) return data.data;
    return [];
  }

  function renderMatches(matchList) {
    let currentLeague = "";

    matchList.forEach((match, index) => {
      const league = getLeague(match);
      const home = getHomeTeam(match);
      const away = getAwayTeam(match);
      const time = getMatchTime(match);

      if (league !== currentLeague) {
        currentLeague = league;
        const leagueEl = document.createElement("div");
        leagueEl.className = "league dynamic-item";
        leagueEl.textContent = `🏆 ${league}`;
        leftPanel.appendChild(leagueEl);
      }

      const matchEl = document.createElement("div");
      matchEl.className = "match dynamic-item";
      matchEl.setAttribute("data-index", index);

      matchEl.innerHTML = `
        <input type="checkbox" class="match-checkbox">
        <div>
          <div class="teams">${escapeHtml(home)} vs ${escapeHtml(away)}</div>
          <div class="time">${escapeHtml(time)}</div>
        </div>
      `;

      matchEl.addEventListener("click", (e) => {
        if (e.target.classList.contains("match-checkbox")) return;

        const checkbox = matchEl.querySelector(".match-checkbox");
        checkbox.checked = !checkbox.checked;
        updateSelectAllState();
      });

      const checkbox = matchEl.querySelector(".match-checkbox");
      checkbox.addEventListener("change", () => {
        updateSelectAllState();
      });

      leftPanel.appendChild(matchEl);
    });
  }

  function getLeague(match) {
    return (
      match.league ||
      match.competition ||
      match.country ||
      match.tournament ||
      "Diğer"
    );
  }

  function getHomeTeam(match) {
    return (
      match.home_team ||
      match.home ||
      match.team1 ||
      match.homeTeam ||
      "Ev Sahibi"
    );
  }

  function getAwayTeam(match) {
    return (
      match.away_team ||
      match.away ||
      match.team2 ||
      match.awayTeam ||
      "Deplasman"
    );
  }

  function getMatchTime(match) {
    return (
      match.time ||
      match.hour ||
      match.kickoff ||
      match.match_time ||
      "Saat bilinmiyor"
    );
  }

  function removeOldMatchList() {
    document.querySelectorAll(".dynamic-item").forEach((el) => el.remove());
  }

  function showLoading() {
    const loading = document.createElement("div");
    loading.className = "dynamic-item";
    loading.style.marginTop = "14px";
    loading.style.color = "#8a7fb0";
    loading.textContent = "Maçlar yükleniyor...";
    leftPanel.appendChild(loading);
  }

  function showEmpty() {
    const empty = document.createElement("div");
    empty.className = "dynamic-item";
    empty.style.marginTop = "14px";
    empty.style.color = "#8a7fb0";
    empty.textContent = "Bugün için maç bulunamadı.";
    leftPanel.appendChild(empty);
  }

  function showError() {
    const error = document.createElement("div");
    error.className = "dynamic-item";
    error.style.marginTop = "14px";
    error.style.color = "#ff6b81";
    error.textContent = "Maçlar alınamadı.";
    leftPanel.appendChild(error);
  }

  function toggleSelectAll() {
    const checkboxes = document.querySelectorAll(".match-checkbox");

    if (!checkboxes.length) return;

    allSelected = !allSelected;

    checkboxes.forEach((checkbox) => {
      checkbox.checked = allSelected;
    });

    selectAllButton.textContent = allSelected ? "❌ Seçimi Kaldır" : "✔ Tümünü Seç";
  }

  function updateSelectAllState() {
    const checkboxes = document.querySelectorAll(".match-checkbox");

    if (!checkboxes.length) {
      allSelected = false;
      selectAllButton.textContent = "✔ Tümünü Seç";
      return;
    }

    const checkedCount = Array.from(checkboxes).filter((cb) => cb.checked).length;

    if (checkedCount === checkboxes.length) {
      allSelected = true;
      selectAllButton.textContent = "❌ Seçimi Kaldır";
    } else {
      allSelected = false;
      selectAllButton.textContent = "✔ Tümünü Seç";
    }
  }

  function escapeHtml(text) {
    return String(text)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  refreshButton.addEventListener("click", loadTodayMatches);
  selectAllButton.addEventListener("click", toggleSelectAll);

  loadTodayMatches();
});
