if __name__ == "__main__":
    from src.tools.question_picker import question_picker
    output = question_picker({
        "difficulty": "medium",
        "taxonomy": "understanding"
    })
    print(output)

