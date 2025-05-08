class MessageFormatter:
    @staticmethod
    def format_message(data, models_with_cons):
        return f"""
        📝 AI Survey Response

        👤 Name: {data['name']}
        📧 Email: {data['email']}
        🎂 Birthdate: {data['birthdate']}
        🎓 Education: {data['education']}
        🏙️ City: {data['city']}
        ⚧️ Gender: {data['gender']}

        🤖 AI Models Tried:
        {', '.join(data['ai_models'])}

        ⚠️ Cons:
        {models_with_cons}

        ✅ Use Case:
        {data['use_case']}
        """