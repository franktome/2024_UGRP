# plot vehicle bounding box on clustered image

# resize bounding box
original_size = (720, 1280)
new_size = (256, 512)

height_scale = new_size[0] / original_size[0]
width_scale = new_size[1] / original_size[1]

def resize_vehicle_coordinates(vehicle_coords, height_scale, width_scale):
    resized_coords = {}
    for key, coords in vehicle_coords.items():
        x1, y1, x2, y2 = coords
        x1_new = x1 * width_scale
        y1_new = y1 * height_scale
        x2_new = x2 * width_scale
        y2_new = y2 * height_scale
        resized_coords[key] = np.array([x1_new, y1_new, x2_new, y2_new], dtype=np.float32)
    return resized_coords

resized_vehicles = resize_vehicle_coordinates(points, height_scale, width_scale)

# 각 vehicle bounding box의 밑변 중점 좌표 계산
midpoints1 = {}
for vehicle, coords in resized_vehicles.items():
    x1, y1, x2, y2 = coords
    midpoint = ((x1 + x2) / 2, y2)
    midpoints1[vehicle] = midpoint

# plot 
lane_image = clustered_img
print(lane_image.shape)
for key, (x1, y1, x2, y2) in resized_vehicles.items():
    cv2.rectangle(lane_image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
    cv2.putText(lane_image, key.replace("vehicle", ''), (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)


# 밑변 중점 좌표 그리기
for vehicle, midpoint in midpoints1.items():
    print(f'{vehicle}: {midpoint}')
    cv2.circle(lane_image, (int(midpoint[0]), int(midpoint[1])), 5, (255, 255, 255), -1)

plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(lane_image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
