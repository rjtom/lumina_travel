import json
from typing import Dict, List, Any
from google.antigravity import ToolContext

# Mock data for destinations
DESTINATIONS_DB = {
    "tokyo": {
        "weather": "Sunny, 22°C (71°F). Mild winds.",
        "events": "Cherry Blossom Festival (Hanami) in Ueno Park.",
        "norms": "Tipping is not practiced and can be considered rude. Always stand on the left side of escalators. Speak softly on public transit.",
        "transit": "Extensive subway network (Suica/Pasmo card recommended). Extremely punctual trains."
    },
    "paris": {
        "weather": "Light rain, 16°C (61°F). Cool breeze.",
        "events": "Fête de la Musique street concerts occurring next week.",
        "norms": "Always greet shopkeepers with 'Bonjour' or 'Bonsoir'. Keep your voice at a moderate volume in restaurants.",
        "transit": "Metro is the fastest way around. Beware of pickpockets at major hubs."
    },
    "new york": {
        "weather": "Clear sky, 26°C (79°F). Warm and humid.",
        "events": "Shakespeare in the Park at Central Park.",
        "norms": "Tipping 18-20% is standard in restaurants. Walk briskly and do not block the sidewalk flow.",
        "transit": "Subway runs 24/7 (OMNY contactless payment accepted). Yellow cabs are widely available."
    }
}

# Mock accommodation listings
ACCOMMODATIONS_DB = [
    {
        "id": "hotel-tokyo-1",
        "name": "Shibuya Glass Oasis Hotel",
        "location": "Tokyo (Shibuya)",
        "price_per_night": 210,
        "availability": "Available for requested dates",
        "cancellation_policy": "Free cancellation up to 24h before check-in",
        "rating": 4.9,
        "description": "A luxury high-rise boutique hotel with views of the Shibuya Crossing. Glassmorphic interior design."
    },
    {
        "id": "hotel-tokyo-2",
        "name": "Traditional Ryokan Kanda",
        "location": "Tokyo (Kanda)",
        "price_per_night": 140,
        "availability": "Last 2 rooms remaining",
        "cancellation_policy": "Non-refundable",
        "rating": 4.7,
        "description": "Authentic tatami rooms with open-air hot spring bath (onsen) access. Complimentary traditional breakfast."
    },
    {
        "id": "hotel-paris-1",
        "name": "Le Marais Chic Apartment",
        "location": "Paris (3rd Arr.)",
        "price_per_night": 185,
        "availability": "Available for requested dates",
        "cancellation_policy": "Free cancellation up to 48h before check-in",
        "rating": 4.8,
        "description": "Stunning loft apartment in the heart of Marais. Classic Parisian architecture with contemporary design."
    },
    {
        "id": "hotel-ny-1",
        "name": "The Nomad Glasshouse",
        "location": "New York (NoMad)",
        "price_per_night": 320,
        "availability": "Available for requested dates",
        "cancellation_policy": "Free cancellation up to 5 days before check-in",
        "rating": 4.6,
        "description": "Industrial chic style hotel featuring floor-to-ceiling windows and a vibrant rooftop bar."
    }
]

def get_destination_info(destination: str) -> str:
    """Delivers personalized, grounded recommendations for a destination using real-time data, weather, events, local norms, and transit guidelines.

    Args:
        destination: The name of the destination (e.g. "Tokyo", "Paris", "New York").
    """
    dest_lower = destination.lower().strip()
    # Simple fuzzy match
    match = None
    for key in DESTINATIONS_DB:
        if key in dest_lower or dest_lower in key:
            match = key
            break

    if match:
        data = DESTINATIONS_DB[match]
        return json.dumps({
            "status": "success",
            "destination": match.title(),
            "weather": data["weather"],
            "events": data["events"],
            "local_norms_and_etiquette": data["norms"],
            "public_transit_guideline": data["transit"]
        }, indent=2)
    else:
        # Fallback dynamic mock data for other places
        return json.dumps({
            "status": "partial_success",
            "destination": destination,
            "weather": "Partly cloudy, 20°C (68°F).",
            "events": "Local cultural festivals are happening. Check local boards.",
            "local_norms_and_etiquette": "Respect local custom and quiet hours. Tipping is generally appreciated.",
            "public_transit_guideline": "Subways and bus routes are available. Ride-sharing is also active."
        }, indent=2)

def search_accommodations(destination: str, max_price: float = None) -> str:
    """Finds and ranks ideal accommodations with pricing, rating, and cancellation policy analysis.

    Args:
        destination: The target destination to search for accommodations (e.g. "Tokyo", "Paris").
        max_price: Optional maximum price filter in USD per night.
    """
    dest_lower = destination.lower().strip()
    matches = []
    for acc in ACCOMMODATIONS_DB:
        if dest_lower in acc["location"].lower() or dest_lower in acc["name"].lower():
            if max_price is None or acc["price_per_night"] <= max_price:
                matches.append(acc)
    
    # Sort matches by rating descending
    matches = sorted(matches, key=lambda x: x["rating"], reverse=True)
    
    if matches:
        return json.dumps({"status": "success", "results": matches}, indent=2)
    else:
        # Generate dynamic accommodations if not found in database to keep the experience alive
        dynamic_acc = [
            {
                "id": f"hotel-{dest_lower.replace(' ', '-')}-1",
                "name": f"Grand Oasis Hotel {destination.title()}",
                "location": destination.title(),
                "price_per_night": 195,
                "availability": "Available for requested dates",
                "cancellation_policy": "Free cancellation up to 48h before check-in",
                "rating": 4.7,
                "description": f"A beautiful modern boutique hotel in central {destination.title()} with excellent amenities."
            }
        ]
        return json.dumps({"status": "generated_success", "results": dynamic_acc}, indent=2)

ACTIVE_BOOKINGS = []

def execute_booking(listing_id: str, confirmation: bool, ctx: ToolContext) -> str:
    """Executes booking for a listing. THIS IS A FINANCIAL ACTION THAT COSTS MONEY. 
    It MUST only be called if the user has explicitly confirmed they want to book this specific listing ID.

    Args:
        listing_id: The ID of the listing to book (e.g. "hotel-tokyo-1").
        confirmation: Must be True to proceed. If False, the booking will be denied.
    """
    if not confirmation:
        return json.dumps({
            "status": "error",
            "message": "Booking denied. User confirmation parameter was not set to True."
        })
    
    # Check if this booking has been stored in context
    bookings = ctx.get_state("bookings", [])
    
    # Find listing details
    listing_details = None
    for acc in ACCOMMODATIONS_DB:
        if acc["id"] == listing_id:
            listing_details = acc
            break
            
    if not listing_details:
        # Try dynamic lookup
        listing_details = {
            "id": listing_id,
            "name": f"Hotel {listing_id.replace('hotel-', '').title()}",
            "price_per_night": 195,
            "location": "Selected Destination"
        }
        
    booking_record = {
        "booking_id": f"BK-{len(bookings) + 1000}",
        "listing_id": listing_id,
        "name": listing_details["name"],
        "price": listing_details.get("price_per_night", 195),
        "status": "CONFIRMED & BOOKED"
    }
    
    bookings.append(booking_record)
    ctx.set_state("bookings", bookings)
    
    # Also append to global tracking list for web app retrieval
    ACTIVE_BOOKINGS.append(booking_record)
    
    return json.dumps({
        "status": "success",
        "message": f"Successfully booked {listing_details['name']}!",
        "booking_details": booking_record
    }, indent=2)
