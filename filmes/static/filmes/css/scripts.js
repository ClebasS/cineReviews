function aumentarImagem(img) {
  img.style.transform = "scale(1.1)";
  img.style.transition = "transform 0.5s ease";
}

function diminuirImagem(img) {
  img.style.transform = "scale(1)";
  img.style.transition = "transform 0.5s ease";
}

function iniciartRating() {
  const stars = document.querySelectorAll('.stars label');

  stars.forEach((star, index) => {
    star.addEventListener('click', () => {
      stars.forEach((s, i) => {
        if (i <= index) {
          s.style.color = '#FFD700';
        } else {
          s.style.color = '#ccc';
        }
      });
    });
    star.addEventListener('mouseenter', () => {
      stars.forEach((s, i) => {
        if (i <= index) {
          s.style.color = '#FFD700';
        } else {
          s.style.color = '#ccc';
        }
      });
    });

    star.addEventListener('mouseleave', () => {
      const avaliacao = document.querySelector('input[name="avaliacao"]:checked');
      if (avaliacao) {
        const index = parseInt(avaliacao.value) - 1;
        stars.forEach((s, i) => {
          if (i <= index) {
            s.style.color = '#FFD700';
          } else {
            s.style.color = '#ccc';
          }
        });
      } else {
        stars.forEach((s) => {
          s.style.color = '#ccc';
        });
      }
    });
  });
}

function atualizarRating(avaliacao) {
  const stars = document.querySelectorAll('.stars label');
  const inputRating = document.querySelector(`input[name="avaliacao"][value="${avaliacao}"]`);
  if (inputRating) {
    inputRating.checked = true;
    const index = parseInt(avaliacao) - 1;
    stars.forEach((s, i) => {
      if (i <= index) {
        s.style.color = '#FFD700';
      } else {
        s.style.color = '#ccc';
      }
    });
  }
}

function exibirRating(rating, commentId) {
  const stars = document.querySelectorAll(`#comentario-${commentId} .stars input`);
  const labels = document.querySelectorAll(`#comentario-${commentId} .stars label`);
  for (let i = 0; i < rating; i++) {
    labels[i].style.color = '#FFD700';
  }
  for (let i = rating; i < stars.length; i++) {
    labels[i].style.color = '#ccc';
  }
}

function manipularBotao(btn, utilizadorId, csrfToken){
  if (btn.classList.contains("follow-button")) {
    seguir(btn, utilizadorId, csrfToken)
  } if (btn.classList.contains("unfollow-button")) {
    unfollow(btn, utilizadorId, csrfToken)
  } if (btn.innerText === "Rebaixar a utilizador") {
    demote(btn, utilizadorId, csrfToken)
  } if (btn.innerText === "Banir utilizador") {
    ban(btn, utilizadorId, csrfToken)
  }
}
function seguir(btn, utilizadorId, csrfToken) {
  fetch(`/filmes/${utilizadorId}/seguiruser`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrfToken},
  })
      .then(response => response.json())
      .then(data => {
        btn.classList.remove(data.follow);  // Remove mystyle class
        btn.classList.add(data.unfollow);
      })
}
function unfollow(btn, utilizadorId, csrfToken) {
  fetch(`/filmes/${utilizadorId}/deixarseguir`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrfToken},
  })
      .then(response => response.json())
      .then(data => {
        btn.classList.remove(data.unfollow);  // Remove mystyle class
        btn.classList.add(data.follow);
      })
}

function demote(btn, utilizadorId, csrfToken) {
  fetch(`/filmes/${utilizadorId}/demotemoderador`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrfToken},
  })
      .then(response => response.json())
      .then(data => {
        btn.innerText = data.novo_texto_botao
      })
}

function ban(btn, utilizadorId, csrfToken) {
  fetch(`/filmes/${utilizadorId}/banuser`, {
    method: 'POST',
    headers: {'X-CSRFToken': csrfToken},
  })
      .then(response => response.json())
      .then(data => {
        btn.style.display = data.nome_style
      })
}

