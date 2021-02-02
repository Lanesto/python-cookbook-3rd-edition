if __name__ == "__main__":
    from my_package.spam import data

    print(data.decode("utf-8"))

    import pkgutil

    data = pkgutil.get_data("my_package", "some_data.dat")
    print(data.decode("utf-8"))
