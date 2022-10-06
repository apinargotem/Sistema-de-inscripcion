
def total_carrito(request):
    total = 0
    totalc=0
    if request:
        if "carrito" in request.session.keys():
            for car in request.session["carrito"]:
                total += float(car["acumulado"])
                totalc += int(car["cantidad"])
    return {"total_carrito": total, "total_cantidad":totalc}

