document.addEventListener('DOMContentLoaded', function() {
    // Initialize button and offset variables
    const triviaBtn = document.getElementById('load-more-trivia-btn');
    if (!triviaBtn) return; // Not on this page — nothing to wire up

    let triviaOffset = parseInt(triviaBtn.getAttribute('data-offset'));
    const triviaUrl = triviaBtn.getAttribute('data-url');

    // Completion flag to track if all trivia has been loaded
    let triviaComplete = false;

    // Trivia button click handler
    triviaBtn.addEventListener('click', function() {
        $.ajax({
            url: triviaUrl,
            data: { 'offset': triviaOffset },
            dataType: 'json',
            success: function(data) {
                if (data.length > 0) {
                    $('#trivia-container').empty();
                    for (let i = 0; i < data.length; i++) {
                        $('#trivia-container').append('<div class="trivia col-md-16 fs-4 bg-light bg-gradient text-center shadow-sm p-3 my-3 rounded border">' + data[i].text + '</div>');
                    }
                    triviaOffset += data.length;

                } else {
                    triviaComplete = true;
                    $('#load-more-trivia-btn').hide();
                    $('#trivia-container .trivia').hide();
                    checkCompletionTrivia();
                }
            }
        });
    });

    // Trivia completion check
    function checkCompletionTrivia() {
        if (triviaComplete) {
            showCongratulationsModalTrivia();
        }
    }

    // Trivia modal
    function showCongratulationsModalTrivia() {
        const modal = document.getElementById('congratulations-modal-trivia');
        if (modal) modal.style.display = 'block';

        const successSound = document.getElementById('success-sound-trivia');
        if (successSound) successSound.play();

        if (navigator.vibrate) {
            navigator.vibrate(200);
        }
    }

    // Change button text for trivia — overrides the inline onclick="changeTriviaButtonText()"
    // from the HTML with this properly-scoped version (the global one referenced by the
    // inline attribute doesn't exist, since this is defined inside this closure).
    function changeTriviaButtonText() {
        triviaBtn.textContent = "Więcej porad";
    }
    triviaBtn.onclick = changeTriviaButtonText;
});