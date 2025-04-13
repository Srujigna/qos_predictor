from django.shortcuts import render
from django.http import JsonResponse
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler



def form_page(request):
    # Render the form template
    return render(request, 'integrated_form_results.html')

def predict(request):
    if request.method == 'POST':
        try:
            # Load the model
            model = joblib.load('predictor/random_forest_qos_model.pkl')

            # Collect the inputs
            signal_strength = float(request.POST['Signal_Strength'])
            required_bandwidth = float(request.POST['Required_Bandwidth'])
            allocated_bandwidth = float(request.POST['Allocated_Bandwidth'])
            resource_allocation = float(request.POST['Resource_Allocation'])
            cpu_utilization = float(request.POST['CPU_Utilization'])
            memory_utilization = float(request.POST['Memory_Utilization'])
            distance_from_bs = float(request.POST['Distance_from_BS'])

            # One-hot encode categorical inputs
            slice_type = request.POST['Slice_Type']
            slice_encoded = [1, 0] if slice_type == 'URLLC' else [0, 1]

            application_type = request.POST['Application_Type']
            application_types = [
                'Background_Download', 'Emergency_Service', 'File_Download', 'IoT_Temperature',
                'Online_Gaming', 'Streaming', 'Video_Call', 'Video_Streaming',
                'VoIP_Call', 'Voice_Call', 'Web_Browsing'
            ]
            app_encoded = [1 if application_type == app else 0 for app in application_types]

            slice_priority = request.POST['Slice_Priority']
            slice_priority_encoded = [1, 0] if slice_priority == 'High' else [0, 1]

            time_of_day = request.POST['Time_of_Day']
            time_of_day_encoded = [1, 0] if time_of_day == 'Morning' else [0, 1]

            weather_conditions = request.POST['Weather_Conditions']
            weather_conditions_encoded = [1 if weather_conditions == weather else 0 for weather in ['Cloudy', 'Rainy', 'Sunny']]

            user_mobility = request.POST['User_Mobility']
            user_mobility_encoded = [1 if user_mobility == mobility else 0 for mobility in ['Driving', 'Stationary', 'Walking']]

            # Combine all features
            input_data = [
                signal_strength, required_bandwidth, allocated_bandwidth, resource_allocation,
                cpu_utilization, memory_utilization, distance_from_bs
            ] + slice_encoded + app_encoded + slice_priority_encoded + time_of_day_encoded + weather_conditions_encoded + user_mobility_encoded

            # Prepare the input array
            input_array = np.array(input_data).reshape(1, -1)

            # Predict
            prediction_scaled = model.predict(input_array)

            # Reverse scale the predictions (if needed)
            scaler_targets = MinMaxScaler()
            scaler_targets.fit(np.array([[0.0, 0.0, 0.05], [110.0, 21.047, 25.0]]))  # Use original ranges
            prediction_original = scaler_targets.inverse_transform(prediction_scaled)

            latency = round(prediction_original[0][0], 2)
            jitter = round(prediction_original[0][1], 2)
            throughput = round(prediction_original[0][2], 2)
            

            # Render the result template
            return render(request, 'integrated_form_results.html', {
                'latency': latency,
                'jitter': jitter,
                'throughput': throughput
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'error': 'Invalid request method. Use POST.'})

def calculate_thresholds(input_features):
    """
    Calculate thresholds based on input features using a rule-based approach.

    Args:
        input_features (dict): A dictionary of form inputs.

    Returns:
        dict: A dictionary containing thresholds for latency, jitter, and throughput.
    """
    # Default thresholds (fallback values)
    thresholds = {
        'Latency': 100.0,  # Default latency threshold (ms)
        'Jitter': 10.0,    # Default jitter threshold (ms)
        'Throughput': 5.0  # Default throughput threshold (Mbps)
    }

    # Rules based on Slice Type
    slice_type = input_features.get('Slice_Type', '').strip()
    if slice_type == 'URLLC':  # Ultra-Reliable Low-Latency Communications
        thresholds['Latency'] = 5.0
        thresholds['Jitter'] = 1.0
        thresholds['Throughput'] = 10.0
    elif slice_type == 'eMBB':  # Enhanced Mobile Broadband
        thresholds['Latency'] = 50.0
        thresholds['Jitter'] = 5.0
        thresholds['Throughput'] = 20.0
    elif slice_type == 'mMTC':  # Massive Machine-Type Communications
        thresholds['Latency'] = 200.0
        thresholds['Jitter'] = 15.0
        thresholds['Throughput'] = 2.0

    # Rules based on Application Type
    app_type = input_features.get('Application_Type', '').strip()
    if app_type == 'Background Download':
        thresholds['Latency'] = 80.0
        thresholds['Jitter'] = 12.0
        thresholds['Throughput'] = 10.0
    elif app_type == 'Emergency Service':
        thresholds['Latency'] = 10.0
        thresholds['Jitter'] = 2.0
        thresholds['Throughput'] = 15.0
    elif app_type == 'File Download':
        thresholds['Latency'] = 70.0
        thresholds['Jitter'] = 10.0
        thresholds['Throughput'] = 12.0
    elif app_type == 'IoT Temperature':
        thresholds['Latency'] = 200.0
        thresholds['Jitter'] = 15.0
        thresholds['Throughput'] = 1.0
    elif app_type == 'Online Gaming':
        thresholds['Latency'] = 30.0
        thresholds['Jitter'] = 5.0
        thresholds['Throughput'] = 20.0
    elif app_type == 'Streaming':
        thresholds['Latency'] = 50.0
        thresholds['Jitter'] = 8.0
        thresholds['Throughput'] = 25.0
    elif app_type == 'Video Call':
        thresholds['Latency'] = 40.0
        thresholds['Jitter'] = 6.0
        thresholds['Throughput'] = 8.0
    elif app_type == 'Video Streaming':
        thresholds['Latency'] = 50.0
        thresholds['Jitter'] = 8.0
        thresholds['Throughput'] = 20.0
    elif app_type == 'VoIP Call':
        thresholds['Latency'] = 30.0
        thresholds['Jitter'] = 4.0
        thresholds['Throughput'] = 5.0
    elif app_type == 'Voice Call':
        thresholds['Latency'] = 40.0
        thresholds['Jitter'] = 5.0
        thresholds['Throughput'] = 3.0
    elif app_type == 'Web Browsing':
        thresholds['Latency'] = 100.0
        thresholds['Jitter'] = 15.0
        thresholds['Throughput'] = 2.0

    # Rules based on Time of Day
    time_of_day = input_features.get('Time_of_Day', '').strip()
    if time_of_day == 'Morning':
        thresholds['Latency'] *= 0.9  # Decrease latency by 10% in the morning
        thresholds['Throughput'] *= 1.1  # Increase throughput by 10%

    # Rules for Weather Conditions (Optional)
    weather_conditions = input_features.get('Weather_Conditions', '').strip()
    if weather_conditions == 'Rainy':
        thresholds['Latency'] *= 1.3  # Increase latency by 30%
        thresholds['Jitter'] *= 1.4  # Increase jitter by 40%
    elif weather_conditions == 'Cloudy':
        thresholds['Latency'] *= 1.1  # Increase latency by 10%
        thresholds['Jitter'] *= 1.2  # Increase jitter by 20%
    elif weather_conditions == 'Sunny':
        thresholds['Throughput'] *= 1.1  # Increase throughput by 10%

    # Rules for User Mobility (Optional)
    user_mobility = input_features.get('User_Mobility', '').strip()
    if user_mobility == 'Driving':
        thresholds['Latency'] *= 1.5  # Increase latency by 50%
        thresholds['Jitter'] *= 2.0  # Double the jitter
    elif user_mobility == 'Walking':
        thresholds['Latency'] *= 0.8  # Decrease latency by 20%
    elif user_mobility == 'Stationary':
        thresholds['Jitter'] *= 0.7  # Decrease jitter by 30%

    return thresholds
