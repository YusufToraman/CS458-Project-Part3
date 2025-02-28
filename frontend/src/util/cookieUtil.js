const getCookie = (name) => {
    const value = document.cookie
        .split("; ")
        .find((row) => row.startsWith(name + "="))
        ?.split("=")[1];
    return value ? JSON.parse(decodeURIComponent(value)) : null;
}

const saveUser = (user) => {
    document.cookie = `user=${JSON.stringify(user)}; samesite=strict; path=/`;
}

const removeUser = () => {
    document.cookie = "user=; samesite=strict; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
}


const CookieUtil = {
    getCookie,
    saveUser,
    removeUser,
};

export default CookieUtil;