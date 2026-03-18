from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from fish.decorator import login_required, login_authenticated
from django.db.models import DateField
from django.db.models.functions import Cast
from django.views.decorators.cache import never_cache
from fish.recommendation.lda_model import predict_food
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import UserLogin, FishSpecies, Recommendation, FoodType, RecentHistory
from django.contrib import messages


# Create your views here.
@never_cache
@login_authenticated
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "admin":
            request.session['user_id'] = 999
            request.session['username'] = "admin"
            return redirect('admin_dashboard')
        
        else:
            try:
                user = UserLogin.objects.get(username=username)

                # Check if account is active
                if not user.is_active:
                    messages.error(request, "Account is disabled")
                    return redirect('login')

                # Verify password
                if check_password(password, user.password):
                    # Create session
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    user.last_login_time = timezone.now()
                    user.save(update_fields=["last_login_time"])
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username or password")

            except UserLogin.DoesNotExist:
                messages.error(request, "Invalid username or password")

    return render(request, "login.html")

@never_cache
@login_required
def admin_dashboard(request):

    water_qs = FishSpecies.objects.values("water_type").annotate(count = Count("id"))
    water_labels = [i["water_type"] for i in water_qs]
    water_data = [i["count"] for i in water_qs]

    user_data = UserLogin.objects.annotate(date=Cast("created_at", DateField())).values("date").annotate(count=Count("id")).order_by("date")
    user_dates = [str(item["date"]) for item in user_data]
    user_counts = [item["count"] for item in user_data]

    pending = Recommendation.objects.filter(status = False)

    return render(request, "admin_dashboard.html", {
        "water_labels": water_labels,
        "water_data": water_data,
        "user_dates": user_dates,
        "user_counts": user_counts,
        "pending": pending
    })

@never_cache
@login_required
def approve(request, id):
    req = Recommendation.objects.get(id = id)
    req.status = True
    req.save()
    return redirect('admin_dashboard')

@never_cache
@login_required
def add_fish(request):
    if request.method == "POST":
        common_name = request.POST.get("common_name")
        scientific_name = request.POST.get("scientific_name")
        water_type = request.POST.get("water_type")
        threat_status = request.POST.get("threat_status")
        taxonomy = request.POST.get("taxonomy")
        habitat = request.POST.get("habitat")
        description = request.POST.get("description")
        fish_img = request.FILES.get("fish_img")

        fish = FishSpecies.objects.create(
            common_name = common_name,
            scientific_name = scientific_name,
            taxonomy_family = taxonomy,
            habitat = habitat,
            water_type = water_type,
            threatened_status = threat_status,
            fish_img = fish_img,
            description = description
        )
        fish.save()
        messages.success(request, "Account created Successfully!")
        return redirect('add_fish')

    return render(request, 'add_fish.html')

@never_cache
@login_required
def edit_fish(request, id):
    fish = FishSpecies.objects.get(id = id)
    if request.method == "POST":
        common_name = request.POST.get("common_name")
        scientific_name = request.POST.get("scientific_name")
        water_type = request.POST.get("water_type")
        threat_status = request.POST.get("threat_status")
        taxonomy = request.POST.get("taxonomy")
        habitat = request.POST.get("habitat")
        description = request.POST.get("description")
        fish_img = request.FILES.get("fish_img")

        fish.common_name = common_name
        fish.scientific_name = scientific_name
        fish.water_type = water_type
        fish.threatened_status = threat_status
        fish.taxonomy_family = taxonomy
        fish.habitat = habitat
        fish.description = description
        if fish_img is not None:
            fish.fish_img = fish_img
        fish.save()
        return redirect('fish_list')
    return render(request, "edit_fish.html", {'fish': fish})

@never_cache
@login_required
def user_profiles(request):
    users = UserLogin.objects.all().order_by('-is_active')
    query = request.GET.get("q")

    if query:
        users = users.filter(
            Q(username__icontains = query)
        )

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "user_profiles.html", {"page_obj": page_obj})

@never_cache
@login_required
def user_activation(request, id):
    user = UserLogin.objects.get(id = id)
    if user.is_active == True:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('user_profiles')

@never_cache
@login_authenticated
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        location = request.POST.get("location")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if UserLogin.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = UserLogin.objects.create(
            username = username,
            email = email,
            password = make_password(password1),
            location = location
        )
        user.save()

        messages.success(request, "Account created Successfully!")
        return redirect('login')

    return render(request, "register.html")

@never_cache
def logout(request):
    username = request.session.get("username")

    if username == 'admin':
        request.session.flush()
        return redirect('login')
    else:
        user = UserLogin.objects.get(username=username)

        user.last_logout_time = timezone.now()
        user.save(update_fields=["last_logout_time"])
        request.session.flush()
        return redirect('login')

@never_cache
@login_required
def home(request):
    # Water Type
    water_qs = FishSpecies.objects.values("water_type").annotate(count = Count("id"))
    water_labels = [i["water_type"] for i in water_qs]
    water_data = [i["count"] for i in water_qs]

    # Habitat
    habitat_qs = FishSpecies.objects.values("habitat").annotate(count=Count("id")).order_by("-count")[:5]
    habitat_labels = [i["habitat"] for i in habitat_qs]
    habitat_data = [i["count"] for i in habitat_qs]

    # Threatened status
    threat_qs = FishSpecies.objects.values("threatened_status").annotate(count = Count("id"))
    threat_labels = [i["threatened_status"] for i in threat_qs]
    threat_data = [i["count"] for i in threat_qs]
    return render(request, 'dashboard.html', {
        "water_labels": water_labels,
        "water_data": water_data,
        "habitat_labels": habitat_labels,
        "habitat_data": habitat_data,
        "threat_labels": threat_labels,
        "threat_data": threat_data,
    })

@never_cache
@login_required
def fish_list(request):
    if request.session.get('user_id') == 999:
        template = "admin_base.html"
    else:
        template = "base.html"
    fishes = FishSpecies.objects.all()
    query = request.GET.get("q")
    water_type = request.GET.get("water_type")

    if query:
        fishes = fishes.filter(
            Q(common_name__icontains = query) |
            Q(scientific_name__icontains = query)
        )

    if water_type:
        fishes = fishes.filter(water_type=water_type)

    paginator = Paginator(fishes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'fish_list.html', {'page_obj': page_obj, 'template': template})

@never_cache
@login_required
def fish_details(request, id):
    fish = get_object_or_404(FishSpecies, id = id)
    username = request.session.get("username")
    user = UserLogin.objects.get(username = username)
    previous_page = request.META.get("HTTP_REFERER")

    if 'fish_list' in previous_page:
        print(previous_page)
        history = RecentHistory.objects.create(
            user = user,
            fish = fish,
            action = 1
        )
        history.save()

        user_history = RecentHistory.objects.filter(user = user).order_by("-created_at")
        if user_history.count() > 5:
            user_history.last().delete()
    else:
        history = RecentHistory.objects.order_by("-created_at").first()

    nodes = []
    edges = []

    main_fish_id = f"fish-{fish.id}"

    nodes.append({
        "id": main_fish_id,
        "label": fish.common_name,
        "group": "fish"
    })

    # Relationship hub nodes
    related_rel_id = f"rel-related-{fish.id}"

    # Habitat
    habitats = {h.strip() for h in fish.habitat.split("&")}

    if habitats:
        habitat_rel_id = f"rel-habitat-{fish.id}"

        nodes.append({
            "id": habitat_rel_id,
            "label": "Habitat",
            "group": "relation"
        })

        edges.append({
            "from": main_fish_id,
            "to": habitat_rel_id
        })

        for habitat in habitats:
            habitat_node_id = f"habitat-{habitat}"

            if habitat_node_id not in {n["id"] for n in nodes}:
                nodes.append({
                    "id": habitat_node_id,
                    "label": habitat,
                    "group": "habitat"
                })

            edges.append({
                "from": habitat_rel_id,
                "to": habitat_node_id
            })
    
    # Alias
    aliases = fish.aliases.all()

    if aliases.exists():
        alias_rel_id = f"rel-alias-{fish.id}"

        nodes.append({
            "id": alias_rel_id,
            "label": "Aliases",
            "group": "relation"
        })

        edges.append({
            "from": main_fish_id,
            "to": alias_rel_id
        })

        for alias in aliases:
            alias_node_id = f"alias-{alias.id}"

            nodes.append({
                "id": alias_node_id,
                "label": alias.alias_name,
                "group": "alias"
            })

            edges.append({
                "from": alias_rel_id,
                "to": alias_node_id
            })

    # Fish Relationship
    base_habitats = {h.strip() for h in fish.habitat.split("&")}
    related_fishes = []

    for rel in FishSpecies.objects.exclude(id=fish.id):
        rel_habitats = {h.strip() for h in rel.habitat.split("&")}

        if base_habitats.intersection(rel_habitats):
            related_fishes.append(rel)

    if related_fishes:
        related_rel_id = f"rel-related-{fish.id}"

        nodes.append({
            "id": related_rel_id,
            "label": "Shared Habitat",
            "group": "relation"
        })

        edges.append({
            "from": main_fish_id,
            "to": related_rel_id
        })

        for rel in related_fishes[:6]:
            rid = f"fish-{rel.id}"

            nodes.append({
                "id": rid,
                "label": rel.common_name,
                "group": "related_fish"
            })

            edges.append({
                "from": related_rel_id,
                "to": rid
            })

    return render(request, 'fish_details.html', {'fish': fish, 'nodes': nodes, 'edges': edges, 'history': history})

@never_cache
@login_required
def recommend(request, h_id, id):
    fish = FishSpecies.objects.get(id = id)
    context = {
        "fish": fish,
        "show_result": False
    }

    if request.method == "POST":
        farm_type = request.POST.get("farm_type")
        farm_size = float(request.POST.get("farm_size"))
        water_temperature = float(request.POST.get("water_temperature"))

        history = RecentHistory.objects.get(id = h_id)
        history.action = 2
        history.created_at = timezone.now()
        history.save()

        # LDA Logic
        predicted_food, confidence = predict_food(fish.common_name, fish.water_type, farm_type, farm_size, water_temperature)
        food = FoodType.objects.get(food_name = predicted_food)

        context.update({
            "show_result": True,
            "recommended_food": predicted_food,
            "confidence": confidence,
            "food": food,
            "history": history
        })

    return render(request, 'recommend.html', context)

@never_cache
@login_required
def save_and_req(request, h_id, fish_id):
    if request.method == "POST":
        fish = FishSpecies.objects.get(id = fish_id)

        food = request.POST.get("food_id")
        food_id = FoodType.objects.get(id = food)

        id = request.session['user_id']
        user = UserLogin.objects.get(id = id)

        history = RecentHistory.objects.get(id = h_id)
        history.action = 3
        history.created_at = timezone.now()
        history.save()

        farm_type = request.POST.get("farm_type_re")
        farm_size = float(request.POST.get("farm_size_re"))
        water_temperature = float(request.POST.get("water_temperature_re"))
        recommended_food = request.POST.get("recommended_food")
        confidence = float(request.POST.get("confidence"))
        

        Recommendation.objects.create(
            user=user,
            fish=fish,
            food = food_id,
            farm_type=farm_type,
            farm_size=farm_size,
            water_temperature=water_temperature,
            recommended_food_name=recommended_food,
            confidence=confidence
        )
    messages.success(request, "Fish Food ordered Sucessfully!")
    return redirect("recommend", h_id = history.id, id = fish.id)

@never_cache
@login_required
def profile(request):
    username = request.session.get('username')
    last_duration = None

    if not username:
        return redirect("login")
    details = UserLogin.objects.get(username = username)
    history = RecentHistory.objects.filter(user = details).order_by("-created_at")
    
    if request.method == "POST":
        user_img = request.FILES.get("profile_img")

        if user_img:
            details.image = user_img
            details.save()

        return redirect('profile')
    

    if details.last_login_time and details.last_logout_time:
        last_duration = details.last_login_time - details.last_logout_time
    if last_duration:
        seconds = int(last_duration.total_seconds())
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        formatted_duration = f"{hours} hours {minutes} minutes"
    else:
        formatted_duration = None

    content = {
        'username': details.username,
        'email': details.email,
        'location': details.location,
        'img': details.image,
        'last_duration': formatted_duration,
        'history': history
    }

    return render(request, 'profile.html', content)

@never_cache
@login_required
def request_log(request):
    user = request.session['user_id']
    log = Recommendation.objects.filter(user = user).order_by('status')

    paginator = Paginator(log, 10) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'recommend_log.html', {'page_obj': page_obj})

@never_cache
@login_required
def request_cancel(request):
    if request.method == "POST":
        id = request.POST.get('log_id')
        del_request = Recommendation.objects.get(id = id)
        del_request.delete()
    
    return redirect('request_log')
