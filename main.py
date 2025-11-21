def get_crop_market_prices(crop_name: str, location: str = "India") -> dict:
    """
    Get current market prices for a specific crop using web search
    """
    try:
        # Search for current market prices
        search_query = f"{crop_name} market price today {location} mandi rates"
        search_results = tavily.search(query=search_query, max_results=5)
        
        if not search_results.get('results'):
            return {"error": "No market data found"}
        
        # Extract relevant price information
        market_data = {
            "crop": crop_name,
            "location": location,
            "search_date": datetime.now().strftime("%Y-%m-%d"),
            "sources": []
        }
        
        for result in search_results['results'][:3]:
            market_data["sources"].append({
                "title": result.get('title', ''),
                "url": result.get('url', ''),
                "content_snippet": result.get('content', '')[:200] + "..."
            })
        
        return market_data
    
    except Exception as e:
        return {"error": f"Market data retrieval failed: {str(e)}"}

def analyze_price_trends(crop_name: str, location: str = "India") -> dict:
    """
    Analyze price trends for a crop over recent months
    """
    try:
        # Search for price trend analysis
        search_query = f"{crop_name} price trend analysis last 6 months {location} agriculture market"
        search_results = tavily.search(query=search_query, max_results=5)
        
        if not search_results.get('results'):
            return {"error": "No trend data found"}
        
        trend_analysis = {
            "crop": crop_name,
            "location": location,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "trend_insights": []
        }
        
        for result in search_results['results'][:3]:
            trend_analysis["trend_insights"].append({
                "source": result.get('title', ''),
                "url": result.get('url', ''),
                "insight": result.get('content', '')[:300] + "..."
            })
        
        return trend_analysis
    
    except Exception as e:
        return {"error": f"Price trend analysis failed: {str(e)}"}

def get_demand_supply_analysis(crop_name: str, location: str = "India") -> dict:
    """
    Get demand and supply analysis for a specific crop
    """
    try:
        # Search for demand-supply information
        search_query = f"{crop_name} demand supply analysis {location} agriculture market forecast"
        search_results = tavily.search(query=search_query, max_results=5)
        
        if not search_results.get('results'):
            return {"error": "No demand-supply data found"}
        
        demand_supply = {
            "crop": crop_name,
            "location": location,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "market_conditions": []
        }
        
        for result in search_results['results'][:3]:
            demand_supply["market_conditions"].append({
                "source": result.get('title', ''),
                "url": result.get('url', ''),
                "analysis": result.get('content', '')[:300] + "..."
            })
        
        return demand_supply
    
    except Exception as e:
        return {"error": f"Demand-supply analysis failed: {str(e)}"}

def get_seasonal_market_advice(crop_name: str, current_month: int = None) -> dict:
    """
    Get seasonal market advice for optimal selling times
    """
    if current_month is None:
        current_month = datetime.now().month
    
    try:
        # Search for seasonal market patterns
        month_name = datetime(2024, current_month, 1).strftime("%B")
        search_query = f"{crop_name} best time to sell seasonal market patterns {month_name} India agriculture"
        search_results = tavily.search(query=search_query, max_results=5)
        
        if not search_results.get('results'):
            return {"error": "No seasonal data found"}
        
        seasonal_advice = {
            "crop": crop_name,
            "current_month": month_name,
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
            "seasonal_insights": []
        }
        
        for result in search_results['results'][:3]:
            seasonal_advice["seasonal_insights"].append({
                "source": result.get('title', ''),
                "url": result.get('url', ''),
                "advice": result.get('content', '')[:300] + "..."
            })
        
        return seasonal_advice
    
    except Exception as e:
        return {"error": f"Seasonal analysis failed: {str(e)}"}

def comprehensive_market_analysis(crop_name: str, location: str = "India") -> dict:
    """
    Perform comprehensive market analysis combining all functions
    """
    try:
        analysis = {
            "crop": crop_name,
            "location": location,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_prices": get_crop_market_prices(crop_name, location),
            "price_trends": analyze_price_trends(crop_name, location),
            "demand_supply": get_demand_supply_analysis(crop_name, location),
            "seasonal_advice": get_seasonal_market_advice(crop_name)
        }
        
        # Generate summary recommendations
        analysis["recommendations"] = generate_market_recommendations(analysis)
        
        return analysis
    
    except Exception as e:
        return {"error": f"Comprehensive analysis failed: {str(e)}"}

def generate_market_recommendations(analysis_data: dict) -> list:
    """
    Generate actionable recommendations based on market analysis
    """
    recommendations = []
    
    # Basic recommendations based on available data
    if "error" not in analysis_data.get("current_prices", {}):
        recommendations.append("✅ Current market prices have been analyzed")
    
    if "error" not in analysis_data.get("price_trends", {}):
        recommendations.append("📈 Price trend analysis indicates market patterns")
    
    if "error" not in analysis_data.get("demand_supply", {}):
        recommendations.append("📊 Demand-supply conditions have been evaluated")
    
    if "error" not in analysis_data.get("seasonal_advice", {}):
        recommendations.append("🗓️ Seasonal timing factors have been considered")
    
    # General farming advice
    recommendations.extend([
        "💡 Monitor daily mandi rates for optimal selling decisions",
        "📱 Use government agriculture apps for official price updates",
        "🤝 Consider collective bargaining with other farmers",
        "📦 Explore direct-to-consumer sales channels",
        "🌾 Plan crop diversification based on market trends"
    ])
    
    return recommendations

# ============================
# LANGCHAIN TOOLS
# ============================

# Tool 1: Get Current Market Prices
price_check_tool = Tool(
    name="Check Crop Prices",
    func=lambda x: json.dumps(get_crop_market_prices(x), indent=2),
    description="Get current market prices for a specific crop. Input should be crop name (e.g., 'tomato', 'wheat', 'rice')."
)

# Tool 2: Price Trend Analysis
trend_analysis_tool = Tool(
    name="Analyze Price Trends",
    func=lambda x: json.dumps(analyze_price_trends(x), indent=2),
    description="Analyze price trends for a crop over recent months. Input should be crop name."
)

# Tool 3: Demand Supply Analysis
demand_supply_tool = Tool(
    name="Demand Supply Analysis",
    func=lambda x: json.dumps(get_demand_supply_analysis(x), indent=2),
    description="Get demand and supply analysis for a crop. Input should be crop name."
)

# Tool 4: Seasonal Market Advice
seasonal_advice_tool = Tool(
    name="Seasonal Market Advice",
    func=lambda x: json.dumps(get_seasonal_market_advice(x), indent=2),
    description="Get seasonal market advice for optimal selling times. Input should be crop name."
)

# Tool 5: Comprehensive Market Analysis
comprehensive_analysis_tool = Tool(
    name="Comprehensive Market Analysis",
    func=lambda x: json.dumps(comprehensive_market_analysis(x), indent=2),
    description="Perform complete market analysis including prices, trends, demand-supply, and seasonal advice. Input should be crop name."
)

# ============================
# CREWAI AGENTS
# ============================

# Agent 2: Market Analysis Expert
market_analyst = Agent(
    role="Agricultural Market Analyst",
    goal="Provide comprehensive market analysis and trading recommendations to help farmers make informed selling decisions",
    backstory=(
        "You are an experienced agricultural market analyst with deep knowledge of crop pricing, "
        "seasonal trends, demand-supply dynamics, and trading strategies. You help farmers maximize "
        "their profits by providing data-driven market insights and timing recommendations."
    ),
    tools=[
        price_check_tool,
        trend_analysis_tool,
        demand_supply_tool,
        seasonal_advice_tool,
        comprehensive_analysis_tool
    ],
    verbose=True,
    allow_delegation=False
)

# Agent 3: Trading Strategy Advisor
trading_advisor = Agent(
    role="Crop Trading Strategy Advisor",
    goal="Develop optimal selling strategies and timing recommendations based on market conditions",
    backstory=(
        "You are a specialized trading advisor focused on agricultural commodities. You analyze "
        "market data to recommend the best times to sell crops, identify profitable market "
        "opportunities, and suggest risk management strategies for farmers."
    ),
    tools=[comprehensive_analysis_tool, seasonal_advice_tool],
    verbose=True,
    allow_delegation=False
)

# ============================
# CREWAI TASKS
# ============================

# Task 2: Market Analysis Task
market_analysis_task = Task(
    description=(
        "Analyze the current market conditions for the specified crop. "
        "Include current prices, recent trends, demand-supply analysis, and seasonal factors. "
        "Provide actionable recommendations for farmers."
    ),
    expected_output=(
        "Comprehensive market report with current prices, trend analysis, demand-supply conditions, "
        "seasonal recommendations, and specific advice for optimal selling strategies."
    ),
    agent=market_analyst
)

# Task 3: Trading Strategy Task
trading_strategy_task = Task(
    description=(
        "Based on the market analysis, develop specific trading strategies and timing recommendations. "
        "Consider seasonal patterns, price volatility, and market opportunities to maximize farmer profits."
    ),
    expected_output=(
        "Detailed trading strategy with optimal selling times, price targets, risk management advice, "
        "and alternative market channels for the specified crop."
    ),
    agent=trading_advisor
)

# ============================
# INTEGRATION FUNCTION
# ============================

def run_market_analysis(crop_name: str = "tomato"):
    """
    Run the complete market analysis crew for a specific crop
    """
    # Update task descriptions with the specific crop
    market_analysis_task.description = f"Analyze the current market conditions for {crop_name}. Include current prices, recent trends, demand-supply analysis, and seasonal factors. Provide actionable recommendations for farmers."
    
    trading_strategy_task.description = f"Based on the market analysis for {crop_name}, develop specific trading strategies and timing recommendations. Consider seasonal patterns, price volatility, and market opportunities to maximize farmer profits."
    
    # Create and run the crew
    market_crew = Crew(
        agents=[market_analyst, trading_advisor],
        tasks=[market_analysis_task, trading_strategy_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = market_crew.kickoff()
    return result

# ============================
# EXAMPLE USAGE
# ============================

if __name__ == "__main__":
    # Example: Analyze tomato market
    crop_to_analyze = "tomato"
    print(f"🔍 Starting market analysis for {crop_to_analyze}...")
    
    # Run individual analysis
    analysis_result = comprehensive_market_analysis(crop_to_analyze)
    print("\n📊 Market Analysis Result:")
    print(json.dumps(analysis_result, indent=2))
    
    # Run full crew analysis
    print(f"\n🤖 Running AI crew analysis for {crop_to_analyze}...")
    crew_result = run_market_analysis(crop_to_analyze)
    print("\n✅ Crew Analysis Complete!")
    print(crew_result)











