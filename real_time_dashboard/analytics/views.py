from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.contrib import messages

from .services import get_stock_price_cached, get_many_quotes
from django.http import JsonResponse
from .services import get_stock_price_cached

def stock_price(request):
    symbol = (request.GET.get('symbol') or 'TSLA').upper()
    try:
        data = get_stock_price_cached(symbol)
        # Map keys for frontend compatibility
        return JsonResponse({
            "symbol": data["symbol"],
            "current_price": data["price"],
            "previous_close": data["price"] - data["change"],
            "change": data["change"],
            "change_percent": data["change_percent"],
        })
    except Exception as e:
        return JsonResponse({"symbol": symbol, "error": str(e)}, status=503)
        
TOP_SYMBOLS = [
    "AAPL","MSFT","GOOGL","AMZN","TSLA",
    "META","NVDA","JPM","NFLX","AMD",
]

def _get_portfolio(request):
    pf = request.session.get("portfolio") or {}
    if not isinstance(pf, dict):
        pf = {}
    return pf

def _save_portfolio(request, pf):
    request.session["portfolio"] = pf
    request.session.modified = True

@require_http_methods(["GET", "POST"])
def dashboard(request):
    pf = _get_portfolio(request)

    if request.method == "POST":
        action = request.POST.get("action")
        sym = (request.POST.get("symbol") or "").upper()
        if action == "add" and sym:
            item = pf.get(sym) or {"symbol": sym, "name": sym, "quantity": 0}
            item["quantity"] = max(1, item["quantity"] + 1)
            pf[sym] = item
            _save_portfolio(request, pf)
            return redirect(reverse("analytics_dashboard"))
        if action == "inc" and sym and sym in pf:
            pf[sym]["quantity"] += 1
            _save_portfolio(request, pf)
            return redirect(reverse("analytics_dashboard"))
        if action == "dec" and sym and sym in pf:
            pf[sym]["quantity"] = max(1, pf[sym]["quantity"] - 1)
            _save_portfolio(request, pf)
            return redirect(reverse("analytics_dashboard"))
        if action == "remove" and sym in pf:
            del pf[sym]
            _save_portfolio(request, pf)
            return redirect(reverse("analytics_dashboard"))
        if action == "clear":
            _save_portfolio(request, {})
            return redirect(reverse("analytics_dashboard"))

    q = (request.GET.get("q") or "").strip()
    search_quote = None
    if q:
        try:
            # treat as symbol first
            search_quote = get_stock_price_cached(q)
            search_quote["name"] = search_quote.get("name") or q.upper()
        except Exception:
            messages.warning(request, "Not found or API limit reached. Try later.")
            search_quote = None

    top_quotes = get_many_quotes(TOP_SYMBOLS)

    portfolio_symbols = list(pf.keys())
    portfolio_quotes = {q["symbol"]: q for q in get_many_quotes(portfolio_symbols)} if portfolio_symbols else {}
    total = 0.0
    for sym, item in pf.items():
        price = portfolio_quotes.get(sym, {}).get("price") or 0.0
        item["price"] = price
        total += price * item.get("quantity", 0)

    context = {
        "top_quotes": top_quotes,
        "search_query": q,
        "search_quote": search_quote,
        "portfolio": pf,
        "portfolio_total": total,
        # Optional: auto-refresh via meta (no JS)
        "refresh_seconds": 15,
    }
    return render(request, "dashboard.html", context)