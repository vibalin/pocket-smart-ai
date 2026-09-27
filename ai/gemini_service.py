from google import genai
from app.config import get_settings


settings = get_settings()

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


# =========================================================
# GEMINI HELPER
# =========================================================

def ask_gemini(prompt):

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )

        if response and response.text:
            return response.text

    except Exception as e:
        print("Gemini Error:", e)

    return None


# =========================================================
# HOME PLANNER
# =========================================================

def generate_home_recommendation(
    budget: float,
    rooms: str,
    style: str,
    priorities: str,
    location: str
):

    prompt = (
        "Create a practical home interior recommendation. "
        f"Budget: ₹{budget}. "
        f"Rooms: {rooms}. "
        f"Style: {style}. "
        f"Priorities: {priorities}. "
        f"Location: {location}. "
        "Give recommendations, estimated prices and budget tips."
    )

    result = ask_gemini(prompt)

    if result:
        return result

    return (
        "HOME INTERIOR RECOMMENDATION\n\n"
        f"Budget: ₹{budget:,.0f}\n"
        f"Rooms: {rooms}\n"
        f"Style: {style}\n"
        f"Location: {location}\n\n"
        "RECOMMENDED PLAN\n\n"
        f"Furniture: ₹{budget * 0.30:,.0f}\n"
        f"Lighting: ₹{budget * 0.10:,.0f}\n"
        f"Furnishings: ₹{budget * 0.15:,.0f}\n"
        f"Storage: ₹{budget * 0.20:,.0f}\n"
        f"Decoration: ₹{budget * 0.15:,.0f}\n"
        f"Other: ₹{budget * 0.10:,.0f}\n\n"
        f"TOTAL: ₹{budget:,.0f}\n\n"
        "BUDGET TIPS\n"
        "1. Buy essential furniture first.\n"
        "2. Compare prices before buying.\n"
        "3. Choose multipurpose furniture.\n\n"
        "Gemini is temporarily unavailable.\n"
        "Local PocketSmart recommendation used."
    )


# =========================================================
# PARTY PLANNER
# =========================================================

def generate_party_recommendation(
    budget: float,
    event_type: str,
    guests: int,
    location: str,
    food_preference: str,
    decoration_style: str,
    priorities: str
):

    prompt = (
        "Create a practical party plan. "
        f"Budget: ₹{budget}. "
        f"Event: {event_type}. "
        f"Guests: {guests}. "
        f"Location: {location}. "
        f"Food: {food_preference}. "
        f"Decoration: {decoration_style}. "
        f"Priorities: {priorities}. "
        "Give food, decoration, cake, photography "
        "and budget tips."
    )

    result = ask_gemini(prompt)

    if result:
        return result

    food = budget * 0.45
    decoration = budget * 0.20
    cake = budget * 0.15
    photography = budget * 0.10
    other = budget * 0.10

    return (
        "PARTY RECOMMENDATION\n\n"
        f"Event: {event_type}\n"
        f"Guests: {guests}\n"
        f"Location: {location}\n\n"
        f"TOTAL BUDGET: ₹{budget:,.0f}\n\n"
        "FOOD\n"
        f"Preference: {food_preference}\n"
        f"Estimated Cost: ₹{food:,.0f}\n\n"
        "DECORATION\n"
        f"Style: {decoration_style}\n"
        f"Estimated Cost: ₹{decoration:,.0f}\n\n"
        "CAKE\n"
        f"Estimated Cost: ₹{cake:,.0f}\n\n"
        "PHOTOGRAPHY / ENTERTAINMENT\n"
        f"Estimated Cost: ₹{photography:,.0f}\n\n"
        "OTHER EXPENSES\n"
        f"Estimated Cost: ₹{other:,.0f}\n\n"
        f"TOTAL: ₹{budget:,.0f}\n\n"
        "BUDGET TIPS\n"
        "1. Choose an affordable venue.\n"
        "2. Order food based on guest count.\n"
        "3. Use simple decorations.\n\n"
        "Gemini is temporarily unavailable.\n"
        "Local PocketSmart recommendation used."
    )


# =========================================================
# JEWELRY PLANNER
# =========================================================

def generate_jewelry_recommendation(
    budget: float,
    occasion: str,
    jewelry_type: str,
    metal: str,
    style: str,
    outfit_description: str,
    location: str
):

    prompt = (
        "Create a practical jewelry recommendation. "
        f"Budget: ₹{budget}. "
        f"Occasion: {occasion}. "
        f"Jewelry Type: {jewelry_type}. "
        f"Metal: {metal}. "
        f"Style: {style}. "
        f"Outfit: {outfit_description}. "
        f"Location: {location}. "
        "Give jewelry suggestions, estimated prices, "
        "outfit matching advice and budget tips."
    )

    result = ask_gemini(prompt)

    if result:
        return result

    main_cost = budget * 0.70
    accessories_cost = budget * 0.15
    other_cost = budget * 0.15

    return (
        "JEWELRY RECOMMENDATION\n\n"
        f"Occasion: {occasion}\n"
        f"Jewelry Type: {jewelry_type}\n"
        f"Metal: {metal}\n"
        f"Style: {style}\n"
        f"Location: {location}\n\n"
        "BUDGET\n"
        f"Total Budget: ₹{budget:,.0f}\n\n"
        "MAIN JEWELRY\n"
        f"Recommended Style: {style}\n"
        f"Estimated Cost: ₹{main_cost:,.0f}\n\n"
        "ACCESSORIES\n"
        "Suggested matching accessories for the outfit.\n"
        f"Estimated Cost: ₹{accessories_cost:,.0f}\n\n"
        "MISCELLANEOUS\n"
        f"Estimated Cost: ₹{other_cost:,.0f}\n\n"
        "OUTFIT MATCH\n"
        f"{outfit_description}\n\n"
        "BUDGET TIPS\n"
        "1. Choose a simple design for a more affordable option.\n"
        "2. Select jewelry that can be reused for different occasions.\n"
        "3. Compare prices before purchasing.\n\n"
        "ESTIMATED TOTAL\n"
        f"₹{budget:,.0f}\n\n"
        "Note:\n"
        "Gemini AI is temporarily unavailable.\n"
        "This recommendation was generated using the "
        "PocketSmart AI jewelry fallback system."
    )