import track


@track.track
def hanoi(n=1, src="A", aux="B", dest="C"):
    if n == 1:
        return
    else:
        hanoi(n=n - 1, src=src, aux=dest, dest=aux)
        hanoi(n=n - 1, src=aux, aux=src, dest=dest)


def main():
    n = int(input())
    hanoi(n=n, src="A", aux="B", dest="C")


if __name__ == "__main__":
    main()
